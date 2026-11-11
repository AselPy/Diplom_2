import allure
import pytest

from data import ErrorMessages
from helpers import update_user, login_user, generate_new_value, generate_random_string


class TestUpdateUser:

    @allure.title('Авторизованный пользователь может изменить поле: {field}')
    @pytest.mark.parametrize('field', ['email', 'name'])
    def test_update_user_field_with_auth_success(self, registered_user, field):
        new_value = generate_new_value(field)

        response = update_user({field: new_value}, registered_user["token"])

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"][field] == new_value

    # Пароль в ответе не возвращается, поэтому проверяем, что с новым паролем можно войти
    @allure.title('Авторизованный пользователь может изменить пароль')
    def test_update_user_password_with_auth_success(self, registered_user):
        new_password = generate_random_string()

        response = update_user({"password": new_password}, registered_user["token"])
        login_response = login_user({"email": registered_user["payload"]["email"], "password": new_password})

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert login_response.status_code == 200

    @allure.title('Без авторизации нельзя изменить поле: {field}')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_update_user_field_without_auth_unauthorized(self, field):
        new_value = generate_new_value(field)

        response = update_user({field: new_value})

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": ErrorMessages.UNAUTHORISED}
