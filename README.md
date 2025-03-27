# Signals

This project explores the behavior of Django signals with respect to synchronization, threading, and database transactions. It includes views and signal handlers to test whether Django signals:
- Execute synchronously or asynchronously
- Run in the same thread as the caller
- Execute within the same database transaction as the caller
- Tests custom Rectangle class implementation.

## Features

- Signal Execution Mode: Check if signals run synchronously by default.

- Thread Behavior: Identify if signals run in the same thread as the caller.

- Database Transaction Handling: Verify if signals execute within the same DB transaction.

- Custom Rectangle Class - Implements an iterable class returning length and width.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/itsmohitnamdeo/signals
   cd django-signals-test
   ```

2. Apply Migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Run Django Server:

   ```bash
   python manage.py runserver
   ```

## API Endpoints & Usage

- Synchronous Signal Execution Test.
- URL: http://127.0.0.1:8000/test-sync/

![test-sync](https://github.com/user-attachments/assets/cd6e2150-b6e3-47a6-9e32-8da472674086)


- Signal Database Transaction Test
- URL: http://127.0.0.1:8000/test-transaction/

![test-transaction](https://github.com/user-attachments/assets/4c6ef3f0-bb71-42b0-9049-8069ca7da926)


- Signal Threading Behavior Test
- URL: http://127.0.0.1:8000/test-thread/

![test-thread](https://github.com/user-attachments/assets/771bc473-5ebc-4dcb-b5c6-23e539a0db3e)


- Rectangle Iterable Class Test
-  URL: http://127.0.0.1:8000/test-rectangle/?length=10&width=5

![test-rectangle](https://github.com/user-attachments/assets/160392f0-0daa-4a04-a1c0-32e7b8d55f81)


## Conclusion
- Django signals run synchronously by default.
- Signals execute in the same thread as the caller unless explicitly dispatched from another thread.
- Signals do not automatically execute inside the same database transaction as the caller.

## Contact

If you have any questions, suggestions, or need assistance related to the CSV-File-Utility-Tool, feel free to reach out to Me.

- MailId - namdeomohit198@gmail.com
- Mob No. - 9131552292
- Portfolio : https://itsmohitnamdeo.github.io
- Linkedin : https://www.linkedin.com/in/mohit-namdeo
