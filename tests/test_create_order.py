import allure

from data import ErrorMessages, INVALID_INGREDIENT_HASH
from helpers import create_order


class TestCreateOrder:

    @allure.title('Авторизованный пользователь может создать заказ с ингредиентами')
    def test_create_order_with_auth_and_ingredients_success(self, registered_user, ingredient_ids):
        response = create_order(ingredient_ids, registered_user["token"])

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert isinstance(body["order"]["number"], int)

    # API принимает заказ и без токена: сервер отвечает 200, это фактическое поведение сервиса
    @allure.title('Без авторизации можно создать заказ с ингредиентами')
    def test_create_order_without_auth_success(self, ingredient_ids):
        response = create_order(ingredient_ids)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert isinstance(body["order"]["number"], int)

    @allure.title('Нельзя создать заказ без ингредиентов')
    def test_create_order_without_ingredients_bad_request(self, registered_user):
        response = create_order([], registered_user["token"])

        assert response.status_code == 400
        assert response.json() == {"success": False, "message": ErrorMessages.INGREDIENTS_REQUIRED}

    # По документации сервер отвечает на невалидный хеш HTML-страницей с ошибкой, а не JSON
    @allure.title('Нельзя создать заказ с неверным хешем ингредиента')
    def test_create_order_with_invalid_ingredient_hash_server_error(self, registered_user):
        response = create_order([INVALID_INGREDIENT_HASH], registered_user["token"])

        assert response.status_code == 500
        assert 'Internal Server Error' in response.text
