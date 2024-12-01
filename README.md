# Django Telegram Authorization Project

Этот проект демонстрирует реализацию авторизации пользователей Django через Telegram-бота. Пользователи могут войти на веб-сайт, используя свой Telegram-аккаунт.

## Содержание

- [Технологии](#технологии)
- [Требования](#требования)
- [Установка](#установка)
- [Настройка](#настройка)
- [Запуск](#запуск)
- [Использование](#использование)
- [Структура проекта](#структура-проекта)
- [Дополнительная информация](#дополнительная-информация)

## Технологии

- Python 3.10+
- Poetry
- Django
- python-telegram-bot
- SQLite (по умолчанию)

## Требования

- Установленный Python 3.10 или выше
- Аккаунт Telegram для создания бота
- Публичный сервер с поддержкой HTTPS (для использования вебхуков, если требуется)
- Git

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/BiqRed/DjangoAuthTGBot.git
cd DjangoAuthTGBot
```

### 2. Создание и активация виртуального окружения

```bash
# Создание виртуального окружения
poetry install

# Активация виртуального окружения
poetry shell
```

## Настройка

### 1. Создание Telegram-бота

1. Откройте Telegram и найдите бота [@BotFather](https://telegram.me/BotFather).
2. Отправьте команду `/newbot` и следуйте инструкциям для создания нового бота.
3. Получите токен API вашего бота.

### 2. Настройка переменных окружения

Для безопасности рекомендуется хранить конфиденциальные данные (например, токен бота и секретный ключ Django) в переменных окружения.

Создайте файл `.env` в корне проекта и добавьте следующие строки:

```env
SECRET_KEY=your-django-secret-key
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
SITE_URL=https://your-domain.com
```

**Примечание:** Замените `your-django-secret-key`, `your-telegram-bot-token` и `https://your-domain.com` на реальные значения.

### 3. Обновление `settings.py`

Убедитесь, что `settings.py` загружает переменные окружения. Для этого используется библиотека `python-decouple`.

Откройте `telegram_auth_project/settings.py` и убедитесь, что он содержит следующие настройки:

```python
from decouple import config
from pathlib import Path

# Построение путей внутри проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ
SECRET_KEY = config('SECRET_KEY')

# Отладка
DEBUG = True

ALLOWED_HOSTS = ['*']  # Настройте для продакшн

# Приложения Django
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auth_app',  # Наше приложение
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'telegram_auth_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Добавим директорию для шаблонов
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Добавлено для доступа к request в шаблонах
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'telegram_auth_project.wsgi.application'

# База данных (используем SQLite для простоты)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Аутентификация
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
]

# Локализация
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Статические файлы
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# URL перенаправления после входа
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')

# URL вашего сайта (используется для создания ссылок)
SITE_URL = config('SITE_URL')
```

### 4. Применение миграций и создание суперпользователя

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Следуйте инструкциям для создания суперпользователя.

## Запуск

### 1. Запуск сервера Django

```bash
python manage.py runserver
```

По умолчанию сервер будет доступен по адресу `http://127.0.0.1:8000/`.

### 2. Запуск Telegram-бота

В отдельном терминале активируйте виртуальное окружение и запустите бота:

```bash
python manage.py runbot
```

**Примечание:** Убедитесь, что бот запущен и работает корректно.

## Использование

1. Перейдите на страницу входа вашего сайта (`http://127.0.0.1:8000/login/`).
2. Зарегистрируйтесь или войдите через стандартный механизм Django.
3. После входа нажмите кнопку "Войти через Telegram".
4. Вы перейдете на страницу с ссылкой на Telegram-бота.
5. Нажмите на ссылку, перейдите в Telegram и отправьте команду `/start`.
6. После успешной авторизации вернитесь на сайт. Страница автоматически обновится и отобразит ваш никнейм из Telegram.

## Структура проекта

```
telegram_auth_project/
├── auth_app/
│   ├── admin.py
│   ├── apps.py
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── runbot.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── ... (миграции)
│   ├── models.py
│   ├── telegram_bot.py
│   ├── templates/
│   │   ├── home.html
│   │   ├── login.html
│   │   └── login_with_telegram.html
│   ├── tests.py
│   └── views.py
├── telegram_auth_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
│   ├── home.html
│   ├── login.html
│   └── login_with_telegram.html
├── static/
│   └── ... (статические файлы, если необходимо)
├── db.sqlite3
├── manage.py
├── requirements.txt
└── .gitignore
```

## Дополнительная информация

- **Безопасность:** В продакшн-среде убедитесь, что `DEBUG=False` и настроены корректные `ALLOWED_HOSTS`.
- **HTTPS:** Для корректной работы Telegram-бота в режиме вебхуков требуется SSL-сертификат. В данном примере используется режим polling, который не требует вебхуков.
- **Переменные окружения:** Используйте переменные окружения для хранения конфиденциальных данных. Не храните их в репозитории.
- **Управление зависимостями:** Обновляйте зависимости регулярно и фиксируйте версии в `requirements.txt`.
