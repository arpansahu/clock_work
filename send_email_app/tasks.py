import time
from random import random

from django.contrib.auth import get_user_model
from celery_progress.backend import ProgressRecorder
from celery_progress.websockets.backend import WebSocketProgressRecorder
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True)
def send_mail_func(self):
    users = get_user_model().objects.all()
    for user in users:
        mail_subject = "Hi! Celery Testing"
        message = "You have received this email as a test message from CLOCK WORK Reminder & Notes"
        to_email = user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=False,
        )
    return "Done"

@shared_task(bind=True)
def send_mail_task(self, emails, headline, content):
    progress_recorder = ProgressRecorder(self)
    for email_no in range(len(emails)):
        mail_subject = headline
        message = content
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[emails[0]],
            fail_silently=False,
        )
        progress_recorder.set_progress(email_no + 1, len(emails), f'Sending Notes to {emails[email_no]}')

    return "Done"


@shared_task(bind=True)
def ws_task(self, number):
    progress_recorder = WebSocketProgressRecorder(self)
    for i in range(number):
        time.sleep(.1)
        progress_recorder.set_progress(i+1, number)
    return int(random()*1000)

@shared_task(bind=True)
def web_socket_send_mail_task(self, emails, headline, content):
    progress_recorder = WebSocketProgressRecorder(self)
    for email_no in range(len(emails)):
        mail_subject = headline
        message = content
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[emails[0]],
            fail_silently=False,
        )
        progress_recorder.set_progress(email_no + 1, len(emails), f'Sending Notes to {emails[email_no]}')

    return "Done"
