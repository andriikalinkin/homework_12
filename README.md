# homework_11

---
## How to launch the project

1. Install dependencies
```
pip install -r requirements.txt
```

2. Make migrations
```
python manage.py makemigrations
python manage.py migrate
```

3. Install Docker. Download "RabbitMQ" official, and run this broker in 1-st terminal window
```
docker -p 5672:5672 --name rabbitmq --rm rabbitmq
```

4. Start django-celery-beat in 2-nd terminal window
```
celery -A <project> beat
```

5. Start Celery in 3-rd terminal window
```
celery -A homework_10 worker -l INFO
```

6. Run Django server in 4-th terminal window
```
python manage.py runserver
```

7. Go to http://127.0.0.1:8000/exchange_rates/ in your browser.