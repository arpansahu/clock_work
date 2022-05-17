
# Clock Works | Django Redis Celery Email Scheduler and Notes Taker

This project provides following features

-Implemented Celery and Redis to Take Notes and Email it.
    
1. Used MailJet in Production to send Emails, at first Gmail with SMTP was using. Since heroku don't allow SMTP activities in the server, MailJet was used 
2. You can see the progress of the task in frontend
3. Progress Bar is Implemented with Ajax as well as Channels


-Implemented Celery Beat to Schedule Emails as Reminders

1. Used Celery beat to Schedule Reminder Emails
2. used asyncio inside Signals Code to avoid interference with sync_to_async
3. As soon as task is completed a notification is send to user about its completion

-Broadcast Notifications using Web Sockets and Channels

-Deployed on Heroku

1. Used Heroku Postgres 
2. Used Daphene

## What is Redis, Celery, Celery Beat, Web Sockets, Channels, Signals, Ajax?
In the below image I will try to explain everything.

![alt text](https://github.com/arpansahu/clock_work/blob/master/explanation.png?raw=true)

1. When a user wants to take notes and want it to email-ed. Then from Django app we send 
    a request to Django View to create and Send a task to Redis/RabbitMQ broker. Then 
    broker will be passing this task to celery. Moreover, since while creating a task we 
    used celery results to save the progress in CELER_RESULT_BACKEND (django-db or redis or rabbitmq).
    So while the task is being executed user can see progress bar via two methods:

    - Using Ajax Call: While the process is not completed you can continuously hit the 
      endpoint to check status fo the task. which eventually increase your server load.
    - Using Web Sockets and channels: As soon as you load the web page you make a web socket 
      protocol connection to the server via handshaking and once the connection is established
      your server can directly send messages to frontend without request from the user end.
      This channel layer is also using Redis for Quick Response. So as soon as there are any changes
      to status of task it is notified to channel and if user is still connected to the channels, will
      be able to see the results in progress bar.

2. When a user wants to Schedule an Email as Reminder then, Via Django Application View, a cron task is created and that is 
   assigned to Celery Beat and as soon as the scheduled time arrived it pass task to broker and then it is finally assinged 
   to celery which finishes the task and at the end of the task, a message is passed through channels to frontend to notify about the completion of task.

3. Admin can broadcast a Notification to all users using django channels and cron tab, admin can schedule the notification 
   at the 
## Tech Stack

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
[![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Javascript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)](https://www.javascript.com/)
[![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/docs/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/docs/)
[![Celery](https://img.shields.io/badge/celery-%2337814A.svg?&style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/en/stable/index.html)
[![RabbitMQ](https://img.shields.io/badge/rabbitmq-%23FF6600.svg?&style=for-the-badge&logo=rabbitmq&logoColor=white")](https://www.rabbitmq.com/)
[![Heroku](https://img.shields.io/badge/-Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)](https://heroku.com/)
[![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://www.github.com/)

## Demo

Available at: http://django-chat-app-version1.herokuapp.com/

Note: Remmber to access this project at http because websockets are not configured to run over https in this project yet. 

admin login details:--
username: admin
password: showmecode
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Installation

Installing Pre requisites
```bash
  pip install -r requirements.txt
```

Create .env File
```bash
  add variables mentioned in .env.example
```

Making Migrations and Migrating them.
```bash
  python manage.py makemigrations
  python manage.py migrate
```

Creating Super User
```bash
  python manage.py createsuperuser
```
Note: if you try to access chat room with just one user it will be throwing error.So after creating a superuser
register from a new user using website and then enter into it. It must have at least two users to chat.

-------------------------

Installing Redis On Local (For ubuntu) for other Os Please refer to their website https://redis.io/
```bash
  curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
  echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
  sudo apt-get update
  sudo apt-get install redis
  sudo systemctl restart redis.service
```
to check if its running or not
```
  sudo systemctl status redis
```
--------------------------

Use these CELERY settings

``` 
CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
```
CELERY_RESULT_BACKEND have been commented, because when we use Django Channels 
with websockets for sending notification, django-db as a backend is synchronous
and thus gives error, Hence we have to use redis or other resources which primarily 
supports asynchronous work flow.
---

Creating Asyn App - create a file named celery.py in project directory.
``` 
import os

from celery import Celery
from celery.schedules import crontab
from decouple import config

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clock_work.settings')

redis_url = config("REDISCLOUD_URL")

app = Celery('clock_work', broker=redis_url, backend=redis_url, include=['tasks.tasks'])

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'send-mail-every-day-at-8': {
        'task': 'send_email_app.tasks.send_mail_func',
        'schedule': crontab(hour=0, minute=38),
        # 'args' : (2,)
    }
}
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

```

set ASGI settings in settings.py
``` 
ASGI_APPLICATION = 'clock_work.routing.application'
```

Uncomment Channel Layers Setting for Local Machine on settings.py, line 137 to 144 
```bash
   CHANNEL_LAYERS = {
     'default': {
         'BACKEND': 'channels_redis.core.RedisChannelLayer',
         'CONFIG': {
             "hosts": [('127.0.0.1', 6379)],
         },
     },
   }
```
Comment Channel Layers Setting for Heroku on settings.py, line 147 to 154 
```bash
   CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [config('REDISCLOUD_URL')],
        },
    },
  }
```

Run Server
```bash
  python manage.py runserver
```

## Deployment on Heroku

Installing Heroku Cli from : https://devcenter.heroku.com/articles/heroku-cli
Create your account in Heroku.

Inside your project directory

Login Heroku CLI
```bash
  heroku login

```

Create Heroku App

```bash
  heroku create [app_name]

```

Push Heroku App
```
    git push heroku master
```

Configure Heroku App
```bash
  heroku config:set GITHUB_USERNAME=joesmith

```
Configuring Django App for Heroku

Install whitenoise 
```
pip install whitenoise 
```

Include it in Middlewares.
```
MIDDLEWARE = [
    # ...
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ...
]
```

Create Procfile and include this code snippet in it.
```
release: python manage.py migrate
web: daphne clock_work.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A clock_work.celery worker -l info
celerybeat: celery -A clock_work beat -l INFO
celeryworker2: celery -A clock_work.celery worker & celery -A clock_work beat -l INFO & wait -n
```
---
In the above Procfile there are three workers required for web, celery and celery beat, but since heroku free
plan only allows upto 2 free dynos we have merged celery and celerybeat into celeryworker2
and from the admin panel of heroku app we can enable just the web and celeryworker2.
---

Comment down Database setting and install 

``` 
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST'),
#         'PORT': config('DB_PORT'),
#     }
# }
```
```
pip install dj-database-url
```

and add these lines below the commented Database settings
``` 
import dj_database_url
DATABASES = {'default': dj_database_url.config(default=config('DATABASE_URL'))}
```

Change CELERY_BROKER_URL from 
``` 
CELERY_BROKER_URL = 'redis://localhost:6379'
```
to
```
CELERY_BROKER_URL=config("REDISCLOUD_URL")
```
## Documentation

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
[![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Javascript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)](https://www.javascript.com/)
[![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/docs/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/docs/)
[![Celery](https://img.shields.io/badge/celery-%2337814A.svg?&style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/en/stable/index.html)
[![RabbitMQ](https://img.shields.io/badge/rabbitmq-%23FF6600.svg?&style=for-the-badge&logo=rabbitmq&logoColor=white")](https://www.rabbitmq.com/)
[![Heroku](https://img.shields.io/badge/-Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)](https://heroku.com/)
[![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://www.github.com/)

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

REDISCLOUD_URL=

SECRET_KEY=

DEBUG=

ALLOWED_HOSTS=

EMAIL_USER=

EMAIL_PASS=

DATABASE_URL=

MAIL_JET_API_KEY=

MAIL_JET_API_SECRET=

ALLOWED_HOSTS=

REDIS_URL=
