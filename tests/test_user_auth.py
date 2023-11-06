import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.label("owner", "KateSh")
@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [("no cookie"), ("no token")]

    with allure.step(f"Prepare data"):
        def setup_method(self):
            data = {'email': 'vinkotov@example.com', 'password': '1234'}

            response1 = MyRequests.post("user/login", data=data)

            self.auth_sid = self.get_cookie(response1, "auth_sid")
            self.token = self.get_headers(response1, "x-csrf-token")
            self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("SmokeTest")
    @allure.description("This test successfully authorize user with correct email and password")
    @allure.testcase("TMS-126")
    def test_auth_user(self):
        response2 = MyRequests.get("user/auth",
                                 headers={"x-csrf-token":self.token},
                                 cookies={"auth_sid":self.auth_sid})
        Assertions.assert_json_value_by_name(response2,
                                             "user_id",
                                             self.user_id_from_auth_method,
                                             "User id from auth method is not equal to user id from check method")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("SmokeTest")
    @allure.description("This test authorizes user without sending tokens or cookies and checks status of this authorization")
    @allure.testcase("TMS-446")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no cookie":
            with allure.step(f"Create user without cookie"):
                response2 = MyRequests.get("user/auth",
                                     headers={"x-csrf-token": self.token})
        else:
            with allure.step(f"Create user without headers"):
                response2 = MyRequests.get("user/auth",
                                     cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(response2,
                                             "user_id",
                                             0,
                                             f"User is authorized with condition {condition}")


