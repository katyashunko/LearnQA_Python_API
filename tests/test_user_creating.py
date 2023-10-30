import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserWithoutAtSigh(BaseCase):
    exclude_params = [("email"), ("password"),("username"), ("firstName"),("lastName")]

    def setup_method(self):
        register_data = self.prepare_registration_data()
        response2 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        self.email = register_data["email"]
        self.username = register_data["username"]
        self.firstName = register_data["firstName"]
        self.lastName = register_data["lastName"]
        self.password = register_data["password"]
        self.user_id = self.get_json_value(response2, "id")

        login_data = {'email': self.email, 'password': self.password}
        response3 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        self.auth_sid = self.get_cookie(response3, "auth_sid")
        self.token = self.get_headers(response3, "x-csrf-token")

        self.short_username = 'k'
        self.long_username = 251 * 'k'
    def test_user_without_at_sigh(self):
        email = 'percovgmail.com'
        register_data = self.prepare_registration_data(email)
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response1, 400)
        Assertions.assert_content(response1, 'Invalid email format')

    def test_user_with_short_name(self):
        response4 = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid},
                                 data = {"username":self.short_username})

        Assertions.assert_status_code(response4, 400)
        Assertions.assert_content(response4, '{"error":"Too short value for field username"}')

    def test_user_with_long_name(self):
        response5 = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid},
                                 data={"username": self.long_username})

        Assertions.assert_status_code(response5, 400)
        Assertions.assert_content(response5, '{"error":"Too long value for field username"}')

    @pytest.mark.parametrize('condition', exclude_params)
    def test_user_without_any_field(self, condition):
        register_data = self.prepare_registration_data_for_all_fields(condition)
        response6 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response6, 400)
        Assertions.assert_content(response6, f"The following required params are missed: {condition}")

