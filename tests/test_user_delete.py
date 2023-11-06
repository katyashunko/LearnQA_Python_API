from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.label("owner", "KateSh")
@allure.epic("Tests for DELETE method")
class TestUserDelete(BaseCase):
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

        login_data = {'email': self.email, 'password': self.password}
        response1 = MyRequests.post("user/login", data=login_data)
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_headers(response1, "x-csrf-token")


    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test tries to delete authorized user with id=2 and gets expected error")
    def test_user_delete_user2(self):
        data = {'email': 'vinkotov@example.com','password': '1234'}
        response1 = MyRequests.post("user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_headers(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")
        response2 = MyRequests.delete(f"user/{user_id}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid})
        Assertions.assert_status_code(response2, 400)
        Assertions.assert_content(response2, 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.')

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("SmokeTest")
    @allure.description("This test successfully deletes authorized user")
    def test_user_real_delete(self):
        response2 = MyRequests.delete(f"user/{self.user_id}",
                                    headers={"x-csrf-token": self.token},
                                    cookies={"auth_sid": self.auth_sid}
                                    )

        Assertions.assert_status_code(response2, 200)
        response3 = MyRequests.get(f"user/{self.user_id}")
        Assertions.assert_status_code(response3, 404)
        Assertions.assert_content(response3, 'User not found')

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test tries to delete unauthorized user when being authorized by another user and gets expected error")
    def test_another_user_delete(self):
        register_data1 = self.prepare_registration_data()
        response = MyRequests.post("user/", data=register_data1)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")
        user_id1 = self.get_json_value(response, "id")
        response3 = MyRequests.delete(f"user/{user_id1}",
                                    headers={"x-csrf-token": self.token},
                                    cookies={"auth_sid": self.auth_sid}
                                    )

        response5 = MyRequests.get(f"user/{self.user_id}")
        print(response5.content)
        Assertions.assert_status_code(response5, 200)


