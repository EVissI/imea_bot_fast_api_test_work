Этот проект представляет собой Telegram-бот с использованием вебхуков, который позволяет пользователям проверять IMEI-номера мобильных устройств с помощью FastAPI и Aiogram.

Бот принимает IMEI, проверяет его на корректность, а затем делает запрос к IMEICheck API, возвращая информацию об устройстве.

🔹 Технологии, используемые в проекте
✅ Python 3.10+
✅ FastAPI (серверная часть)
✅ Aiogram (Telegram-бот)
✅ Aiohttp (асинхронные HTTP-запросы)
✅ SQLAlchemy (работа с базой данных)
✅ JWT (аутентификация)
✅ Pydantic (валидация данных)

🛠 Установка и запуск проекта
1️⃣ Клонирование репозитория
bash
```
git clone https://github.com/your-repo/imei-bot.git
cd imei-bot
```
2️⃣ Создание виртуального окружения
bash
```
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```
3️⃣ Установка зависимостей
bash
```
pip install -r requirements.txt
```
4️⃣ Создание файла .env
Создай .env файл в корне проекта и добавь переменные:

makefile
Копировать
Редактировать
BOT_TOKEN=your-telegram-bot-token
ADMIN_IDS = [admin_list]
IMEI_CHECK_TOKEN=your-imeicheck-api-key
BASE_SITE=https://your-server.com
JWT_SECRET=your-jwt-secret
JWT_ALGORITM = yr coding algoritm
optional:
REDIS_IP: str
REDIS_PORT:str
REDIS_PASSWORD:str
REDIS_USERNAME:str
5️⃣ Запуск приложения
bash
```
uvicorn main:app --port port:int
```
🔹 Функционал бота
📌 Проверка IMEI
Бот принимает IMEI-номер и проверяет его:
Валидирует по алгоритму Луна
Отправляет запрос в API IMEICheck
Возвращает пользователю информацию об устройстве

📌 Административные команды
👮‍♂️ Администраторы могут банить и разбанивать пользователей.

📌 Защита от спама
🛑 Встроен антифлуд-фильтр, предотвращающий частые запросы.

🔹 FastAPI (серверная часть)
🔹 Основные эндпоинты
Метод	URL	Описание
POST	/api/check-imei	Проверяет IMEI через IMEICheck API


🔹 Защита API (JWT-аутентификация)
Для защиты API используется JWT-токен.
JWT - токен создается исключительно при вызове из бота
