import allure
from allure_commons.types import Severity

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("User cases")
@allure.feature("Edit user")
class TestUserEdit(BaseCase):

    @allure.title("Successfully edit own user")
    @allure.story("Positive user editing")
    @allure.severity(Severity.CRITICAL)
    @allure.description(
        "This test checks successful editing of the authorized user's data"
    )
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post(
            "/user/",
            data=register_data
        )

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post(
            "/user/login",
            data=login_data
        )

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        #Get
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    # - Попытаемся изменить данные пользователя, будучи неавторизованными
    @allure.title("Edit user without authorization")
    @allure.story("Authorization restrictions")
    @allure.severity(Severity.CRITICAL)
    @allure.description(
        "This test checks that user data cannot be changed without authorization"
    )
    def test_edit_user_without_auth(self):
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post(
            "/user/",
            data=register_data
        )

        Assertions.assert_code_status(response1, 200)

        user_id = self.get_json_value(response1, "id")
        email = register_data["email"]
        password = register_data["password"]
        old_name = register_data["firstName"]

        # EDIT WITHOUT AUTH
        new_name = "Changed Name"
        response2 = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response2, 400)
        assert response2.json()["error"] == "Auth token not supplied", \
            f"Unexpected response: {response2.text}"

        # LOGIN AS OWNER
        response3 = MyRequests.post(
            "/user/login",
            data={
                "email": email,
                "password": password
            }
        )

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # CHECK THAT NAME WAS NOT CHANGED
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            old_name,
            "User name was changed without authorization"
        )

    # - Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    @allure.title("Attempt to edit another user")
    @allure.story("Authorization restrictions")
    @allure.severity(Severity.BLOCKER)
    @allure.description(
        "This test checks that an authorized user cannot edit another user's data"
    )
    def test_edit_user_other(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post(
            "/user/",
            data=register_data
        )

        Assertions.assert_code_status(response1, 200)

        user_id = self.get_json_value(response1, "id")
        old_name = register_data["firstName"]

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

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.json()["error"] == \
               "Please, do not edit test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response: {response3.text}"

        # LOGIN AS OWNER
        response4 = MyRequests.post(
            "/user/login",
            data={
                "email": register_data["email"],
                "password": register_data["password"]
            }
        )

        owner_auth_sid = self.get_cookie(response4, "auth_sid")
        owner_token = self.get_header(response4, "x-csrf-token")

        # CHECK
        response5 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": owner_token},
            cookies={"auth_sid": owner_auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response5,
            "firstName",
            old_name,
            "User name was changed by another user"
        )

    # - Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    @allure.title("Edit user with invalid email")
    @allure.story("Email validation")
    @allure.severity(Severity.NORMAL)
    @allure.description(
        "This test checks that email cannot be changed to a value without the @ symbol"
    )
    def test_edit_user_with_invalid_email(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post(
            "/user/",
            data=register_data
        )

        Assertions.assert_code_status(response1, 200)

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }

        response2 = MyRequests.post(
            "/user/login",
            data=login_data
        )

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_email = "invalidemail Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.json()["error"] == "Invalid email format", \
            f"Unexpected response: {response3.text}"

        # CHECK
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "email",
            email,
            "User email was changed to invalid value"
        )

    # - Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    @allure.title("Edit user with too short firstName")
    @allure.story("First name validation")
    @allure.severity(Severity.NORMAL)
    @allure.description(
        "This test checks that firstName cannot be changed to a one-character value"
    )
    def test_edit_user_with_short_first_name(self):
        # REGISTER
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post(
            "/user/",
            data=register_data
        )

        Assertions.assert_code_status(response1, 200)

        email = register_data["email"]
        password = register_data["password"]
        old_name = register_data["firstName"]
        user_id = self.get_json_value(response1, "id")

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

        # EDIT
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": "v"}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.json()["error"] == \
               "The value for field `firstName` is too short", \
            f"Unexpected response: {response3.text}"

        # CHECK
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            old_name,
            "User firstName was changed to too short value"
        )
