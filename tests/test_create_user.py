import allure
import pytest

from data import ErrorMessages
from helpers import register_user


class TestCreateUser:

    @allure.title('Можно создать уникального пользователя')
    def test_create_unique_user_success(self, user_payload):
        response = register_user(user_payload)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"] == {"email": user_payload["email"], "name": user_payload["name"]}
        assert body["accessToken"].startswith('Bearer ')

    @allure.title('Нельзя создать пользователя, который уже зарегистрирован')
    def test_create_existing_user_forbidden(self, registered_user):
        response = register_user(registered_user["payload"])

        assert response.status_code == 403
        assert response.json() == {"success": False, "message": ErrorMessages.USER_ALREADY_EXISTS}

    @allure.title('Нельзя создать пользователя без обязательного поля: {missing_field}')
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_create_user_without_required_field_forbidden(self, user_payload, missing_field):
        payload = dict(user_payload)
        payload.pop(missing_field)

        response = register_user(payload)

        assert response.status_code == 403
        assert response.json() == {"success": False, "message": ErrorMessages.REQUIRED_FIELDS}
