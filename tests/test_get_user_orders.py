import allure

from data import ErrorMessages
from helpers import create_order, get_user_orders


class TestGetUserOrders:

    @allure.title('Авторизованный пользователь получает список своих заказов')
    def test_get_orders_authorized_user_returns_own_orders(self, registered_user, ingredient_ids):
        order_number = create_order(ingredient_ids, registered_user["token"]).json()["order"]["number"]

        response = get_user_orders(registered_user["token"])

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert [order["number"] for order in body["orders"]] == [order_number]

    @allure.title('Неавторизованный пользователь не может получить заказы')
    def test_get_orders_unauthorized_user_unauthorized(self):
        response = get_user_orders()

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": ErrorMessages.UNAUTHORISED}
