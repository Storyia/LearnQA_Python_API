import allure
from allure_commons.types import Severity

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("User cases")
@allure.feature("Get user data")
class TestUserGet(BaseCase):

    @allure.title("Get user details without authorization")
    @allure.story("Public user data")
    @allure.severity(Severity.NORMAL)
    @allure.description(
        "This test checks what user data is available without authorization"
    )
    def test_get_user_details_not_auth(self):
        response = MyRequests.get(
            "/user/2"
        )
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_not_has_key(response, "email")
        Assertions.assert_json_not_has_key(response, "firstName")
        Assertions.assert_json_not_has_key(response, "lastName")

    @allure.title("Get own user details")
    @allure.story("Own user data")
    @allure.severity(Severity.CRITICAL)
    @allure.description(
        "This test checks that an authorized user can get all their own data"
    )
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post(
            "/user/login",
            data=data
        )

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.title("Get another user's details")
    @allure.story("Access restrictions")
    @allure.severity(Severity.CRITICAL)
    @allure.description(
        "This test checks that private data of another user is not available"
    )
    def test_get_user_details_auth_as_other_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post(
            "/user/login",
            data=data
        )

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")
        other_user_id = 1

        assert user_id_from_auth_method != other_user_id, \
            "Authorized user and requested user should be different"

        response2 = MyRequests.get(
            f"/user/{other_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_not_has_key(response2, "email")
        Assertions.assert_json_not_has_key(response2, "firstName")
        Assertions.assert_json_not_has_key(response2, "lastName")
