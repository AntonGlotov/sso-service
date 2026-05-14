# SSO Service

Сервис единого входа (SSO) на FastAPI с JWT-авторизацией и RSA токенами.

## Структура

```text
src/
  main.py                 # точка входа приложения
  app/                    # основной пакет приложения
  config/                 # настройки и пути проекта
  dto/                    # Pydantic-схемы и модели данных
  endpoints/              # HTTP API-роуты
  logger/                 # настройка логирования
  pem_utils/              # утилиты для работы с PEM-ключами
  queries/                # запросы к базе данных
  security/               # аутентификация и токены
data/
  user.sqlite3            # рабочая база данных
tests/
  test_api.py             # тесты API
pyproject.toml            # зависимости и конфигурация пакета
README.md                 # документация проекта
```

## Слои

- `src/main.py` - запуск FastAPI-приложения.
- `src/config/__init__.py` - конфигурация проекта, пути к базе, PEM-ключам и логам.
- `src/endpoints/__init__.py` - обработка эндпоинтов `/access_token`, `/refresh_token`, `/users/me`.
- `src/dto/__init__.py` - Pydantic-модели `Token`, `User`, `UserInDB` и т.д.
- `src/security/__init__.py` - проверка паролей, создание/декодирование JWT, зависимости для текущего пользователя.
- `src/pem_utils/__init__.py` - загрузка приватного и публичного RSA-ключей.
- `src/logger/__init__.py` - инициализация и настройка логирования.
- `src/queries/__init__.py` - получение пользователя и другие запросы к БД.
- `tests/test_api.py` - тесты для API.

## Примечания

- Файл `.env` и ключи RSA ожидаются в каталоге `secrets/`.
- Логи записываются в `logs/logs.log`.
- Запуск приложения: `python -m src.main` или `uvicorn src.main:app --reload`.
