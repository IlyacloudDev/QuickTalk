# QuickTalk

[Read in Russian](README_ru.md)

---

QuickTalk is a browser-based messenger for business conversations.

## Table of contents

- [Installation for Windows](#installation-for-windows)
- [Configuration](#configuration)
- [Running](#running)
- [Usage](#usage)

## Installation for Windows
For the correct operation of the project, you need to use **WSL (Windows Subsystem for Linux)**.

1. **Install Redis in WSL** :
   ```bash
   sudo apt update
   sudo apt install redis-server
   ```

2. **Run Redis** :
    ```bash
    sudo service redis-server start
    ```

3. **Transfer the project to a local device** :

   Go to the directory where you want to place the project:
    ```bash
    cd ~
    ```
    Clone the repository:
    ```bash
    git clone https://github.com/IlyacloudDev/QuickTalk.git
    ```
    Go to the project directory:
    ```bash
    cd QuickTalk
    ```

## Configuration
Make sure you have Python and pip installed.

1. **Create a virtual environment** :

    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```
    Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. **Configure the database** :

    Create and apply migrations:
    ```bash
    python manage.py migrate
    ```
    Create a superuser (optional):
    ```bash
    python manage.py createsuperuser
    ```

3. **Collect the static** :

    ```bash
    python manage.py collectstatic
    ```

## Running

1. **To work with WebSockets, run Daphne** :

    ```bash
    daphne -b 0.0.0.0 -p 8000 config.asgi:application
    ```
2. **Opening the project**:

    Open a browser and go to http://127.0.0.1:8000/ to access the application.
    
## Usage

Now you can use QuickTalk to communicate in real time. Create chats and chat with other users!

So far, the ability to add users to group chats is only available through the *admin panel* Django!
