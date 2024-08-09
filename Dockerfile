FROM python:3.10.7

WORKDIR /app

COPY requirements.txt requirements.txt

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8012

CMD bash -c "python manage.py collectstatic --noinput && daphne clock_work.asgi:application -b 0.0.0.0 --port 8012 & celery -A clock_work.celery worker -l info & celery -A clock_work beat -l INFO"