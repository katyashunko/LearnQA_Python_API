from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.label("owner", "KateSh")
@allure.epic("Negative tests for PUT method")
class TestNegativePut(BaseCase):
    def setup_method(self):
        register_data = self.prepare_registration_data()
        response = MyRequests.post("user/", data=register_data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

        self.email = register_data["email"]
        self.username = register_data["username"]
        self.firstName = register_data["firstName"]
        self.lastName = register_data["lastName"]
        self.password = register_data["password"]
        self.user_id = self.get_json_value(response, "id")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test tries to change unauthorized users data and gets expected error")
    def test_changing_data_of_unauthorized_person(self):
        response1 = MyRequests.put(f"user/2",
                                 data={"username": "mouse"})
        Assertions.assert_status_code(response1, 400)
        Assertions.assert_content(response1, 'Auth token not supplied')

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test tries to change unauthorized users data when being authorized by another user and gets expected error")
    def test_changing_data_of_another_person(self):

        login_data = {'email': self.email, 'password': self.password}
        response1 = MyRequests.post("user/login", data=login_data)

        response2 = MyRequests.put(f"user/2",
                                 data={"firstName": "mouse"})

        Assertions.assert_status_code(response2, 400)
        Assertions.assert_content(response2, 'Auth token not supplied')

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test changes authorized users email to the incorrect one and gets expected error")
    @allure.testcase("TMS-451")
    def test_change_on_incorrect_email(self):
        login_data = {'email': self.email, 'password': self.password}
        response2 = MyRequests.post("user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        response1 = MyRequests.put(f"user/{self.user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"email": "perezexample.com"})
        Assertions.assert_status_code(response1, 400)
        Assertions.assert_content(response1, 'Invalid email format')

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test changes authorized users firstNam to the short one and gets expected error")
    @allure.testcase("TMS-455")
    def test_change_firstName_on_short_name(self):
        login_data = {'email': self.email, 'password': self.password}
        response2 = MyRequests.post("user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        response1 = MyRequests.put(f"user/{self.user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": 'k'})
        Assertions.assert_status_code(response1, 400)
        Assertions.assert_content(response1, '{"error":"Too short value for field firstName"}')


