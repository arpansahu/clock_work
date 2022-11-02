FROM python:3.10.7

WORKDIR /app

COPY requirements.txt requirements.txt

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8013

CMD daphne clock_work.asgi:application -b 0.0.0.0 --port 8013 & celery -A borcelle_crm.celery worker -l info & celery -A borcelle_crm beat -l INFO