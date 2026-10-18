import allure
from allure_commons.types import Severity

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("User cases")
@allure.feature("Delete user")
class TestUserDelete(BaseCase):

    # Нельзя удалить пользователя с id 2
    @allure.title("Attempt to delete protected user with ID 2")
    @allure.story("Protected user deletion")
    @allure.severity(Severity.CRITICAL)
    @allure.description(
        "This test checks that protected test user with ID 2 cannot be deleted"
    )
    def test_delete_user_id_2(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        # LOGIN
        response1 = MyRequests.post(
            "/user/login",
            data=data
        )

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")

        assert user_id == 2, \
            f"Unexpected user id: {user_id}"

        # DELETE
        response2 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2, 400)
        assert response2.json()["error"] == \
               "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response: {response2.text}"

        # Проверяем, что пользователь все еще существует
        response3 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_key(response3, "username")

    # Позитивное удаление созданного пользователя
    @allure.title("Successfully delete own user")
    @allure.story("Positive user deletion")
    @allure.severity(Severity.CRITICAL)
    @allure.description(
        "This test checks successful deletion of the authorized user's account"
    )
    def test_delete_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post(
            "/user/",
            data=register_data
        )

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")
        email = register_data["email"]
        password = register_data["password"]

        # LOGIN
        response2 = MyRequests.post(
            "/user/login",
            data={
                "email": email,
                "password": password
            }
        )

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 200)
        assert response3.json()["success"] == "!", \
            f"Unexpected response: {response3.text}"

        # GET AFTER DELETE
        response4 = MyRequests.get(
            f"/user/{user_id}"
        )

        Assertions.assert_code_status(response4, 404)
        assert response4.text == "User not found", \
            f"Unexpected response: {response4.text}"

    # Нельзя удалить пользователя, авторизованным другим пользователем
    @allure.title("Attempt to delete another user")
    @allure.story("Authorization restrictions")
    @allure.severity(Severity.BLOCKER)
    @allure.description(
        "This test checks that an authorized user cannot delete another user's account"
    )
    def test_delete_user_as_other_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post(
            "/user/",
            data=register_data
        )

        Assertions.assert_code_status(response1, 200)

        user_id = self.get_json_value(response1, "id")

        # LOGIN as other user
        login_data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response2 = MyRequests.post(
            "/user/login",
            data=login_data
        )

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        other_user_id = self.get_json_value(response2, "user_id")

        assert other_user_id != user_id, \
            "Authorized user and deleted user should be different"

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.json()["error"] == \
               "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response: {response3.text}"

        response4 = MyRequests.get(
            f"/user/{user_id}"
        )

        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_has_key(response4, "username")
