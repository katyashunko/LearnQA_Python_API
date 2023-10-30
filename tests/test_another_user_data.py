import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestAnotherUserData(BaseCase):
    def test_another_user_data(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        response2 = requests.get("https://playground.learnqa.ru/api/user/2")
        expected_fields = ["id", "email", "firstName", "lastName"]
        Assertions.assert_json_has_no_keys(response2, expected_fields)
        Assertions.assert_json_has_key(response2,"username")