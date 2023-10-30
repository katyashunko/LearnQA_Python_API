import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestNegativePut(BaseCase):
    def setup_method(self):
        register_data = self.prepare_registration_data()
        response = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

        self.email = register_data["email"]
        self.username = register_data["username"]
        self.firstName = register_data["firstName"]
        self.lastName = register_data["lastName"]
        self.password = register_data["password"]
        self.user_id = self.get_json_value(response, "id")

        login_data = {'email': self.email, 'password': self.password}
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_headers(response2, "x-csrf-token")
    def test_changing_data_of_unauthorized_person(self):
        response1 = requests.put(f"https://playground.learnqa.ru/api/user/2",
                                 data={"username": "mouse"})
        Assertions.assert_status_code(response1, 400)
        Assertions.assert_content(response1, 'Auth token not supplied')

    def test_changing_data_of_another_person(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        response2 = requests.put(f"https://playground.learnqa.ru/api/user/2",
                                 data={"firstName": "mouse"})

        Assertions.assert_status_code(response2, 400)
        Assertions.assert_content(response2, 'Auth token not supplied')

    def test_change_on_incorrect_email(self):
        response1 = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid},
                                 data={"email": "perezexample.com"})
        Assertions.assert_status_code(response1, 400)
        Assertions.assert_content(response1, 'Invalid email format')

    def test_change_firstName_on_short_name(self):
        response1 = requests.put(f"https://playground.learnqa.ru/api/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid},
                                 data={"firstName": 'k'})
        Assertions.assert_status_code(response1, 400)
        Assertions.assert_content(response1, '{"error":"Too short value for field firstName"}')


