Installing Pre requisites
```bash
  pip install -r requirements.txt
```

Create .env File and don't forget to add .env to gitignore
```bash
  add variables mentioned in .env.example
```

Making Migrations and Migrating them.
```bash
  python manage.py makemigrations
  python manage.py migrate
```
Run update_data Command
```
  python manage.py update_data
```
Creating Super User
```bash
  python manage.py createsuperuser
```

Installing Redis On Local (For ubuntu) for other Os Please refer to their website https://redis.io/
```bash
  curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
  echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
  sudo apt-get update
  sudo apt-get install redis
  sudo systemctl restart redis.service
```
to check if its running or not
```bash
  sudo systemctl status redis
```

Run Server
```bash
  python manage.py runserver

  or 

  daphne -b 0.0.0.0 -p [PROJECT_DOCKER_PORT] [JENKINS PROJECT NAME].asgi:application
```

Use these CACHE settings

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDISCLOUD_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

Use these Channels Settings

```python
if not DEBUG:
    CHANNEL_LAYERS = {
        'default': {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        }
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(config('REDISCLOUD_URL'))],
            },
        },
    }
```

[STATIC_FILES]

## Custom Django Management Commands

[DJANGO_COMMANDS]