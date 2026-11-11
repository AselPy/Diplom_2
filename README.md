# Diplom_2 — тесты API Stellar Burgers

Автотесты API сервиса [Stellar Burgers](https://qa-stellarburgers.education-services.ru/).

## Что проверяется

- Создание пользователя
- Логин пользователя
- Изменение данных пользователя
- Создание заказа
- Получение заказов конкретного пользователя

## Структура проекта

- `tests/` — тесты, для каждого эндпоинта свой класс.
- `conftest.py` — фикстуры: создание и удаление тестовых пользователей, получение ингредиентов.
- `helpers.py` — запросы к API и генерация тестовых данных.
- `data.py` — тексты ошибок и тестовые данные.
- `urls.py` — адреса API.

## Запуск

```bash
py -m pip install -r requirements.txt
py -m pytest --alluredir=allure-results
```

Просмотр отчёта:

```bash
allure serve allure-results
```
