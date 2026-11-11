import allure
import pytest

from data import ErrorMessages
from helpers import login_user, generate_new_value


class TestLoginUser:

    @allure.title('Можно авторизоваться под существующим пользователем')
    def test_login_existing_user_success(self, registered_user):
        payload = registered_user["payload"]

        response = login_user({"email": payload["email"], "password": payload["password"]})

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"] == {"email": payload["email"], "name": payload["name"]}
        assert body["accessToken"].startswith('Bearer ')

    @allure.title('Нельзя авторизоваться с неверными полями: {wrong_fields}')
    @pytest.mark.parametrize('wrong_fields', ['email', 'password', 'email, password'])
    def test_login_with_wrong_credentials_unauthorized(self, registered_user, wrong_fields):
        payload = {
            "email": registered_user["payload"]["email"],
            "password": registered_user["payload"]["password"]
        }
        for field in wrong_fields.split(', '):
            payload[field] = generate_new_value(field)

        response = login_user(payload)

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": ErrorMessages.INCORRECT_CREDENTIALS}
