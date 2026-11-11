import random
import string

import allure
import requests

from urls import REGISTER_USER, LOGIN_USER, USER, INGREDIENTS, ORDERS


def generate_random_string(length=10):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def generate_user_payload():
    return {
        "email": f'{generate_random_string()}@yandex.ru',
        "password": generate_random_string(),
        "name": generate_random_string()
    }


def generate_new_value(field):
    return f'{generate_random_string()}@yandex.ru' if field == 'email' else generate_random_string()


def build_headers(token):
    return {"Authorization": token} if token else {}


@allure.step('Зарегистрировать пользователя')
def register_user(payload):
    return requests.post(REGISTER_USER, json=payload)


@allure.step('Авторизовать пользователя')
def login_user(payload):
    return requests.post(LOGIN_USER, json=payload)


@allure.step('Изменить данные пользователя')
def update_user(payload, token=None):
    return requests.patch(USER, json=payload, headers=build_headers(token))


@allure.step('Удалить пользователя')
def delete_user(token):
    return requests.delete(USER, headers=build_headers(token))


@allure.step('Получить список ингредиентов')
def get_ingredients():
    return requests.get(INGREDIENTS)


@allure.step('Создать заказ')
def create_order(ingredients, token=None):
    return requests.post(ORDERS, json={"ingredients": ingredients}, headers=build_headers(token))


@allure.step('Получить заказы пользователя')
def get_user_orders(token=None):
    return requests.get(ORDERS, headers=build_headers(token))
