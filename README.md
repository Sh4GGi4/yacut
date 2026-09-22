# YaCut

Сервис коротких ссылок. Превращает длинный адрес в короткий — сгенерированный
автоматически или предложенный пользователем, а ещё загружает файлы на
Яндекс Диск и выдаёт на них короткие ссылки.

## Возможности

- Короткая ссылка из шести символов генерируется автоматически, либо
  пользователь предлагает свой вариант: до 16 латинских букв и цифр.
- Переход по короткой ссылке перенаправляет на исходный адрес.
- На странице `/files` можно загрузить несколько файлов сразу: они
  асинхронно отправляются на Яндекс Диск, для каждого создаётся короткая
  ссылка на скачивание.
- REST API для создания коротких ссылок и получения исходных адресов.

## Стек

- Python 3.11, Flask 3.0 с поддержкой асинхронных вьюх
- Flask-SQLAlchemy, Flask-Migrate, Flask-WTF
- aiohttp — асинхронные запросы к REST API Яндекс Диска
- SQLite

## Запуск проекта

Клонируйте репозиторий и перейдите в него:

```bash
git clone https://github.com/Sh4GGi4/yacut.git
cd yacut
```

Создайте и активируйте виртуальное окружение, установите зависимости:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Создайте в корне проекта файл `.env`:

```
FLASK_APP=yacut
FLASK_DEBUG=1
SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=your_yandex_disk_token
```

`DISK_TOKEN` — OAuth-токен приложения Яндекс Диска с доступами
`cloud_api:disk.app_folder` и `cloud_api:disk.info`. Он нужен только для
загрузки файлов, остальные возможности работают и без него.

Примените миграции и запустите сервер:

```bash
flask db upgrade
flask run
```

Сервис будет доступен по адресу [127.0.0.1:5000](http://127.0.0.1:5000/).

## API

Спецификация описана в файле `openapi.yml`.

Создание короткой ссылки — `POST /api/id/`:

```json
{
  "url": "https://practicum.yandex.ru/",
  "custom_id": "yp"
}
```

Поле `custom_id` необязательное: если его нет, ссылка сгенерируется
автоматически. Ответ с кодом `201`:

```json
{
  "url": "https://practicum.yandex.ru/",
  "short_link": "http://127.0.0.1:5000/yp"
}
```

Получение исходного адреса — `GET /api/id/<short_id>/`:

```json
{
  "url": "https://practicum.yandex.ru/"
}
```

При ошибке API возвращает JSON с описанием в поле `message`.

## Тесты

```bash
pytest
```

## Автор

Набоков Иван Матвеевич — [GitHub](https://github.com/Sh4GGi4)
