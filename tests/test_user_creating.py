import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserCreating(BaseCase):
    exclude_params = [("email"), ("password"),("username"), ("firstName"),("lastName")]

    def test_user_without_at_sigh(self):
        email = 'percovgmail.com'
        register_data = self.prepare_registration_data(email)
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response1, 400)
        Assertions.assert_content(response1, 'Invalid email format')

    def test_user_with_short_name(self):
        register_data = self.check_registration_parameters('1234','k','firstName','lastName')
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response1, 400)
        Assertions.assert_content(response1, "The value of 'username' field is too short")

    def test_user_with_long_name(self):
        register_data = self.check_registration_parameters('1234', 251*'k', 'firstName', 'lastName')
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response1, 400)
        Assertions.assert_content(response1, "The value of 'username' field is too long")

    @pytest.mark.parametrize('condition', exclude_params)
    def test_user_without_any_field(self, condition):
        register_data = self.prepare_registration_data_for_all_fields(condition)
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(response1, 400)
        Assertions.assert_content(response1, f"The following required params are missed: {condition}")

