# QuickTalk

[Читать на английском](README.md)

---

QuickTalk это браузерный мессенджер для бизнес-диалогов.

## Оглавление

- [Установка под Windows](#установка-под-windows)
- [Настройка](#настройка)
- [Запуск](#запуск)
- [Использование](#использование)

## Установка под Windows
Для корректной работы проекта необходимо использовать **WSL (Windows Subsystem for Linux)**.

1. **Установите Redis в WSL** :
   ```bash
   sudo apt update
   sudo apt install redis-server
   ```

2. **Запустите Redis** :
    ```bash
    sudo service redis-server start
    ```

3. **Перенесите проект на локальное устройство** :

    Перейдите в директорию, в которой хотите разместить проект:
    ```bash
    cd ~
    ```
    Клонируйте репозиторий:
    ```bash
    git clone https://github.com/IlyacloudDev/QuickTalk.git
    ```
    Перейдите в директорию проекта:
    ```bash
    cd QuickTalk
    ```

## Настройка
Убедитесь, что у вас установлен Python и pip.

1. **Создайте виртуальное окружение** :

    ```bash
    python -m venv venv
    ```
    Активируйте виртуальное окружение:
    ```bash
    source venv/bin/activate
    ```
    Установите необходимые зависимости:
    ```bash
    pip install -r requirements.txt
    ```

2. **Настройте базу данных** :

    Создайте и примените миграции:
    ```bash
    python manage.py migrate
    ```
    Создайте суперпользователя (по желанию):
    ```bash
    python manage.py createsuperuser
    ```

3. **Соберите статику** :

    ```bash
    python manage.py collectstatic
    ```

## Запуск

1. **Чтобы работать с WebSockets, запустите Daphne** :

    ```bash
    daphne -b 0.0.0.0 -p 8000 config.asgi:application
    ```
2. **Открытие проекта**:

    Откройте браузер и перейдите по адресу http://127.0.0.1:8000/ для доступа к приложению.
    
## Использование

Теперь вы можете использовать QuickTalk для общения в реальном времени. Создавайте чаты и общайтесь с другими пользователями!
