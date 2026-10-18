import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post(
            "/user/",
            data=data
        )

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

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
