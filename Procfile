web: daphne -b 0.0.0.0 --port $PORT chat.asgi:application -v2
chatworker: python manage.py runworker --settings=chat.settings -v2