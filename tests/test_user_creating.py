import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.label("owner", "KateSh")
@allure.epic("Tests for create user with different conditions")
class TestUserCreating(BaseCase):
    exclude_params = [("email"), ("password"),("username"), ("firstName"),("lastName")]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test creates user with incorrect email and gets expected error")
    def test_user_without_at_sigh(self):
        email = 'percovgmail.com'
        register_data = self.prepare_registration_data(email)
        response1 = MyRequests.post("user/", data=register_data)

        Assertions.assert_status_code(response1, 400)
        Assertions.assert_content(response1, 'Invalid email format')

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test creates user with short username and gets expected error")
    def test_user_with_short_name(self):
        register_data = self.check_registration_parameters('1234','k','firstName','lastName')
        response1 = MyRequests.post("user/", data=register_data)

        Assertions.assert_status_code(response1, 400)
        Assertions.assert_content(response1, "The value of 'username' field is too short")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This test creates user with long username and gets expected error")
    def test_user_with_long_name(self):
        register_data = self.check_registration_parameters('1234', 251*'k', 'firstName', 'lastName')
        response1 = MyRequests.post("user/", data=register_data)

        Assertions.assert_status_code(response1, 400)
        Assertions.assert_content(response1, "The value of 'username' field is too long")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("SmokeTest")
    @allure.description("This test creates user with one missing field and gets expected error")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_user_without_any_field(self, condition):
        register_data = self.prepare_registration_data_for_all_fields(condition)
        with allure.step(f"Create user with missing  '{condition}'"):
            response1 = MyRequests.post("user/", data=register_data)

        Assertions.assert_status_code(response1, 400)
        Assertions.assert_content(response1, f"The following required params are missed: {condition}")

