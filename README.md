Этот проект представляет собой Telegram-бот с использованием вебхуков, который позволяет пользователям проверять IMEI-номера мобильных устройств с помощью FastAPI и Aiogram.

Бот принимает IMEI, проверяет его на корректность, а затем делает запрос к IMEICheck API, возвращая информацию об устройстве.

🔹 Технологии, используемые в проекте
✅ Python 3.10+<br>
✅ FastAPI (серверная часть)<br>
✅ Aiogram (Telegram-бот)<br>
✅ Aiohttp (асинхронные HTTP-запросы)<br>
✅ SQLAlchemy (работа с базой данных)<br>
✅ JWT (аутентификация)<br>
✅ Pydantic (валидация данных)<br>

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
bash
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
```
5️⃣ Запуск приложения
bash
```
uvicorn main:app --port port:int
```
🔹 Функционал бота
📌 Проверка IMEI<br>
Бот принимает IMEI-номер и проверяет его:<br>
Валидирует по алгоритму Луна<br>
Отправляет запрос в API IMEICheck<br>
Возвращает пользователю информацию об устройстве<br>

📌 Административные команды<br>
👮‍♂️ Администраторы могут банить и разбанивать пользователей.<br>

📌 Защита от спама<br>
🛑 Встроен антифлуд-фильтр, предотвращающий частые запросы.<br>

🔹 FastAPI (серверная часть)<br>
🔹 Основные эндпоинты<br>

POST	/api/check-imei	<b>Отправляет запрос к <a href='https://imeicheck.net/promo-api'>API imeicheck<a> и возвращает ответ для дальнейшей обработки</b><br>


🔹 Защита API (JWT-аутентификация)<br>
Для защиты API используется JWT-токен.<br>
JWT - токен создается исключительно при вызове из бота, что исключает возможность обращаться из вне<br>
