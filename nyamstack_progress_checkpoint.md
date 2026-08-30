# Nyamstack — progress checkpoint

Актуальный checkpoint проекта после настройки PostgreSQL, конфигурации приложения, SQLAlchemy и Alembic.

---

## 1. Суть проекта

Nyamstack — учебный pet-проект: Telegram-бот для учёта питания и КБЖУ.

Главная цель разработки — не просто быстро получить готовый бот, а постепенно пройти реальные этапы backend-разработки:

- проектирование данных;
- настройка окружения;
- работа с PostgreSQL;
- SQLAlchemy ORM;
- миграции Alembic;
- repositories/services;
- интеграция с aiogram;
- тестирование.

---

## 2. Режим работы

Проект автор реализует самостоятельно.

Агент выполняет роль технического наставника и code-review агента:

- разбивает разработку на маленькие этапы;
- объясняет, зачем нужен каждый этап;
- проверяет реальное состояние репозитория сам;
- проводит review написанного кода;
- прямо указывает ошибки и последствия;
- не пишет готовую реализацию без явного запроса пользователя;
- не меняет рабочий код без явного запроса пользователя;
- может редактировать документацию и явно запрошенные файлы.

Если репозиторий доступен агенту, агент сам читает нужные файлы и выполняет безопасные диагностические команды. Не нужно просить пользователя присылать код или вывод терминала, если это можно проверить самостоятельно.

---

## 3. Окружение и стек

Рабочая среда:

- macOS 26;
- Visual Studio Code;
- Python 3.13;
- виртуальное окружение `.venv`;
- Git-репозиторий связан с `origin`;
- основная ветка — `main`.

Текущий стек:

- Python 3.13;
- aiogram;
- SQLAlchemy 2.x;
- asyncpg;
- PostgreSQL;
- Alembic;
- pydantic-settings;
- Docker / Docker Compose;
- pytest планируется для тестирования.

Добавлен `greenlet`, потому что он требуется SQLAlchemy для async-работы через текущий механизм выполнения.

Redis и LLM-интеграция могут появиться позже, но не добавляются раньше реальной необходимости.

---

## 4. Текущая структура проекта

Основные директории:

```text
app/
  bot/
  config/
  database/
  repositories/

tests/
scripts/
alembic/
```

Назначение слоёв:

- `app/bot` — Telegram-интерфейс, handlers, callbacks, ответы пользователю. Не содержит SQL и основную бизнес-логику.
- `app/services` — будущий слой бизнес-логики. Пока директория может отсутствовать или быть пустой.
- `app/repositories` — будущий слой работы с БД через SQLAlchemy.
- `app/database` — engine, session, ORM-модели, техническая инфраструктура PostgreSQL.
- `app/config` — настройки приложения через `pydantic-settings`.
- `tests` — будущие автоматические тесты.
- `scripts` — временные/служебные диагностические скрипты.
- `alembic` — миграции БД.

Не создавать дополнительные абстрактные слои (`utils`, `common`, `core`, `managers` и т. п.) без необходимости.

---

## 5. Конфигурация и переменные окружения

Используются `.env` и `.env.example`.

`.env`:

- реальные значения;
- не должен попадать в Git.

`.env.example`:

- пример нужных переменных;
- без реальных секретов;
- должен коммититься.

Текущие переменные:

```env
POSTGRES_DB=nyamstack
POSTGRES_USER=nyamstack
POSTGRES_PASSWORD=change_me
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

В `app/config/config.py` создан `Settings` на базе `pydantic-settings`.

Текущий подход:

- в `.env` хранятся отдельные `POSTGRES_*`;
- `database_url` не хранится отдельно;
- `database_url` собирается внутри `Settings` как property.

Формат URL:

```text
postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DB
```

---

## 6. PostgreSQL и Docker Compose

PostgreSQL поднят через `compose.yaml`.

Сервис:

- `postgres`;
- image: `postgres:15`;
- порт: `5432:5432`;
- данные хранятся в volume `pgdata`;
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` берутся из `.env`.

Проверка контейнера:

```bash
docker compose ps
```

Проверка подключения через приложение:

```bash
python -m scripts.check_db
```

Ожидаемый результат:

```text
1 engine ok
1 factory ok
```

---

## 7. SQLAlchemy

В `app/database/connection.py` настроены:

- `engine` через `create_async_engine(settings.database_url)`;
- `async_session_factory` через `async_sessionmaker`;
- `expire_on_commit=False`.

Принятое решение:

- не создавать глобальную открытую session;
- использовать фабрику сессий;
- repositories позже будут получать/создавать `AsyncSession` для операций с БД.

---

## 8. Alembic

Alembic переинициализирован через async-шаблон:

```bash
alembic init -t async alembic
```

В `alembic/env.py` сделано:

- импортируется `settings`;
- `sqlalchemy.url` подставляется из `settings.database_url`;
- импортируется `Base`;
- `target_metadata = Base.metadata`.

Проверка:

```bash
alembic current
```

Команда успешно подключается к PostgreSQL. Миграций пока нет.

`alembic/versions/` — папка для файлов миграций.

---

## 9. ORM-модели

В `app/database/models.py` создан базовый класс:

```python
class Base(DeclarativeBase):
    pass
```

Начата модель `User` для таблицы `users`.

Поля `User` по архитектуре:

- `id` — `INTEGER`, primary key;
- `telegram_id` — `BIGINT`, `NOT NULL`, `UNIQUE`, не primary key;
- `created_at` — дата и время создания пользователя, `NOT NULL`;
- `calorie_target` — `INTEGER`, nullable;
- `protein_target` — `INTEGER`, nullable;
- `fat_target` — `INTEGER`, nullable;
- `carbs_target` — `INTEGER`, nullable.

Важно: на момент checkpoint модель `User` начата, но перед миграцией требуется финальный review и исправление синтаксиса/форматирования, если оно есть в текущем файле.

---

## 10. Основная модель данных проекта

Зафиксированы четыре основные сущности:

- `users`;
- `products`;
- `user_products`;
- `meals`.

### `products`

Общая проверенная база брендовых продуктов.

Поля:

- `id`;
- `name`;
- `brand`;
- `calories_per_100g`;
- `protein_per_100g`;
- `fat_per_100g`;
- `carbs_per_100g`.

На MVP отдельный `usage_count` не нужен.

### `user_products`

Личные продукты пользователя.

Поля:

- `id`;
- `user_id` → `users.id`;
- `name`;
- `brand`, nullable;
- КБЖУ на 100 г;
- `moderation_status` минимум: `pending`, `approved`, `rejected`;
- `global_product_id` → `products.id`, nullable;
- `created_at`.

`global_product_id` не `UNIQUE`: несколько пользовательских записей могут ссылаться на один глобальный продукт.

### `meals`

Факт добавления еды в рацион.

Одна строка `meals` — снимок события:

> кто съел + что съел + сколько + итоговое КБЖУ порции + источник данных + время добавления.

Поля:

- `meal_id`;
- `user_id` → `users.id`;
- `name`;
- `weight_g`;
- `nutrition_source`;
- итоговые `calories`, `protein`, `fat`, `carbs`;
- `created_at`.

`nutrition_source`:

- `approved_product`;
- `user_product`;
- `ai_estimated`.

Исторические `meals` не должны пересчитываться при изменении исходного продукта.

---

## 11. Branded и generic

### `branded`

Конкретный продукт с известными КБЖУ.

Пример:

```text
Простоквашино творог 5% 150 г
```

Логика:

1. искать в личной базе пользователя;
2. затем в общей проверенной базе;
3. пересчитать КБЖУ на фактический вес порции.

### `generic`

Обычное блюдо без точных данных.

Пример:

```text
омлет из 3 яиц
```

Логика:

- оценивается LLM;
- результат помечается как `ai_estimated`;
- после подтверждения сохраняется в `meals`;
- не должен автоматически попадать в `products`.

---

## 12. Правило округления

В базе и промежуточных вычислениях сохраняется достаточная точность.

Округление преимущественно выполняется при отображении пользователю.

Пример:

- две порции по `12.4` г белка;
- точный расчёт: `24.8`;
- отображение: `25` г.

Дневные цели пользователя хранятся целыми числами.

---

## 13. Что уже закрыто

Зафиксированы решения по:

- назначению `users`, `products`, `user_products`, `meals`;
- разделению `branded` и `generic`;
- хранению внутреннего `users.id` отдельно от `telegram_id`;
- раздельным колонкам КБЖУ вместо JSON;
- обязательности КБЖУ для продуктов;
- `nutrition_source`;
- `moderation_status` минимум из трёх состояний;
- хранению снимка КБЖУ в `meals`;
- правилу округления;
- отказу от `usage_count` на MVP;
- использовании async SQLAlchemy + asyncpg;
- хранении `POSTGRES_*` и сборке `database_url` внутри `Settings`;
- использовании async-шаблона Alembic.

---

## 14. Что пока не зафиксировано окончательно

1. `TIMESTAMP` или `TIMESTAMPTZ` для дат.
2. Конкретные размеры `NUMERIC(precision, scale)`.
3. SQL-тип `weight_g`.
4. Способ хранения `moderation_status` и `nutrition_source`.
5. Поведение foreign key при удалении пользователя или продукта.
6. Нужны ли дополнительные индексы.
7. Нужен ли составной `UNIQUE` для продуктов.
8. Как именно реализовать fuzzy search.
9. Как будет устроено удаление и редактирование пользовательских продуктов.
10. Где именно проводить границу транзакции: service layer или repository layer.

---

## 15. Следующая точка разработки

Следующий рабочий шаг:

1. Провести финальный review `app/database/models.py`.
2. Исправить модель `User`, если есть синтаксические ошибки или проблемы типизации.
3. Создать первую миграцию Alembic для `users`.
4. Проверить содержимое миграции до применения.
5. Применить миграцию к PostgreSQL.
6. Проверить, что таблица `users` появилась в базе.

После этого:

1. Реализовать минимальный `UserRepository`.
2. Проверить создание/поиск пользователя.
3. Затем переходить к `products`, `user_products`, `meals`.

Не переходить к aiogram-сценариям, пока базовый слой данных не готов.
