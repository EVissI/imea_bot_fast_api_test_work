Этот проект представляет собой Telegram-бот с использованием вебхуков, который позволяет пользователям проверять IMEI-номера мобильных устройств с помощью FastAPI и Aiogram.

Бот принимает IMEI, проверяет его на корректность, а затем делает запрос к IMEICheck API, возвращая информацию об устройстве.

🔹 Технологии, используемые в проекте\n
✅ Python 3.10+\n
✅ FastAPI (серверная часть)\n
✅ Aiogram (Telegram-бот)\n
✅ Aiohttp (асинхронные HTTP-запросы)\n
✅ SQLAlchemy (работа с базой данных)\n
✅ JWT (аутентификация)\n
✅ Pydantic (валидация данных)\n

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

```
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

```
uvicorn main:app --port port:int
```
🔹 Функционал бота
📌 Проверка IMEI\n
Бот принимает IMEI-номер и проверяет его:\n
Валидирует по алгоритму Луна\n
Отправляет запрос в API IMEICheck\n
Возвращает пользователю информацию об устройстве\n

📌 Административные команды\n
👮‍♂️ Администраторы могут банить и разбанивать пользователей.\n

📌 Защита от спама\n
🛑 Встроен антифлуд-фильтр, предотвращающий частые запросы.\n

🔹 FastAPI (серверная часть)\n
🔹 Основные эндпоинты\n
Метод	URL	Описание\n
POST	/api/check-imei	Проверяет IMEI через IMEICheck API\n


🔹 Защита API (JWT-аутентификация)\n
Для защиты API используется JWT-токен.\n
JWT - токен создается исключительно при вызове из бота
