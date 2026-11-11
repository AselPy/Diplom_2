import pytest

from helpers import generate_user_payload, register_user, login_user, delete_user, get_ingredients


@pytest.fixture
def user_payload():
    """Данные нового пользователя (ещё не создан). Если тест его создаст — пользователь удалится после теста."""
    payload = generate_user_payload()

    yield payload

    response = login_user({"email": payload["email"], "password": payload["password"]})
    if response.status_code == 200:
        delete_user(response.json()["accessToken"])


@pytest.fixture
def registered_user():
    """Зарегистрированный пользователь: данные и accessToken. Удаляется после теста."""
    payload = generate_user_payload()
    token = register_user(payload).json().get("accessToken")

    yield {"payload": payload, "token": token}

    if token:
        delete_user(token)


@pytest.fixture
def ingredient_ids():
    """ID булки и начинки из актуального списка ингредиентов сервиса."""
    ingredients = get_ingredients().json()["data"]
    bun_id = next(item["_id"] for item in ingredients if item["type"] == "bun")
    main_id = next(item["_id"] for item in ingredients if item["type"] == "main")
    return [bun_id, main_id]
