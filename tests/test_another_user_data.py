from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.label("owner", "KateSh")
@allure.epic("This test gets info about user")
class TestAnotherUserData(BaseCase):
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.testcase("TMS-456")
    @allure.description("This test tries to get info about unauthorized user and gets only 'username'")
    def test_another_user_data(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}
        response1 = MyRequests.post("user/login", data=data)

        response2 = MyRequests.get("user/2")
        expected_fields = ["id", "email", "firstName", "lastName"]
        Assertions.assert_json_has_no_keys(response2, expected_fields)
        Assertions.assert_json_has_key(response2,"username")