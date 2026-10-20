import allure
import pytest
from allure_commons.types import Severity

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("User cases")
@allure.feature("User registration")
class TestUserRegister(BaseCase):

    @allure.title("Successful user registration")
    @allure.story("Positive registration")
    @allure.severity(Severity.CRITICAL)
    @allure.description("This test checks successful user registration")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post(
            "/user/",
            data=data
        )

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

        user_id = self.get_json_value(response, "id")

        response_login = MyRequests.post(
            "/user/login",
            data={
                "email": data["email"],
                "password": data["password"]
            }
        )

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        response_get = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response_get,
            "username",
            data["username"],
            "Wrong username after registration"
        )

        Assertions.assert_json_value_by_name(
            response_get,
            "email",
            data["email"],
            "Wrong email after registration"
        )

        Assertions.assert_json_value_by_name(
            response_get,
            "firstName",
            data["firstName"],
            "Wrong firstName after registration"
        )

        Assertions.assert_json_value_by_name(
            response_get,
            "lastName",
            data["lastName"],
            "Wrong lastName after registration"
        )

    @allure.title("Registration with existing email")
    @allure.story("Negative registration")
    @allure.severity(Severity.NORMAL)
    @allure.description("This test checks registration with already existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post(
            "/user/",
            data=data
        )

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected status code {response.status_code}"

    # - Создание пользователя с некорректным email - без символа @
    @allure.title("Registration with invalid email")
    @allure.story("Email validation")
    @allure.severity(Severity.NORMAL)
    @allure.description("This test checks registration with email without @ symbol")
    def test_create_user_with_invalid_email(self):
        email = 'vinkotov'
        data = self.prepare_registration_data(email)
        response = MyRequests.post(
            "/user/",
            data=data
        )
        Assertions.assert_code_status(response, 400)
        assert response.text == "Invalid email format", \
            f"Unexpected response: {response.text}"



    # - Создание пользователя без указания одного из полей - с помощью @ parametrize необходимо проверить, что отсутствие любого
    # параметра не дает зарегистрировать пользователя
    @allure.title("Registration without required field: {missing_field}")
    @allure.story("Required fields validation")
    @allure.severity(Severity.NORMAL)
    @allure.description("This test checks registration without one of required fields")
    @pytest.mark.parametrize(
        "missing_field",
        [
            "password",
            "username",
            "firstName",
            "lastName",
            "email"
        ]
    )
    def test_create_user_field(self, missing_field):
        data = self.prepare_registration_data()
        del data[missing_field]
        response = MyRequests.post(
            "/user/",
            data=data
        )
        Assertions.assert_code_status(response, 400)
        assert response.text == \
               f"The following required params are missed: {missing_field}", \
               f"Unexpected response: {response.text}"

    # - Создание пользователя с очень коротким именем в один символ
    @allure.title("Registration with too short username")
    @allure.story("Username validation")
    @allure.severity(Severity.NORMAL)
    @allure.description("This test checks registration with one-character username")
    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data["username"] = "v"
        response = MyRequests.post(
            "/user/",
            data=data
        )
        Assertions.assert_code_status(response, 400)

        assert response.text == "The value of 'username' field is too short", \
            f"Unexpected response: {response.text}"

    # - Создание пользователя с очень длинным именем - длиннее 250 символов
    @allure.title("Registration with too long username")
    @allure.story("Username validation")
    @allure.severity(Severity.NORMAL)
    @allure.description("This test checks registration with username longer than 250 characters")
    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data["username"] = "v"*251
        response = MyRequests.post(
            "/user/",
            data=data
        )
        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'username' field is too long", \
            f"Unexpected response: {response.text}"
