import json
import time
from random import random
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from celery_progress.backend import ProgressRecorder
from celery_progress.websockets.backend import WebSocketProgressRecorder
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from mailjet_rest import Client

mailjet = Client(auth=(settings.MAIL_JET_API_KEY, settings.MAIL_JET_API_SECRET), version='v3.1')


def send_email_with_template(to_email, subject, template_name, context=None, from_name="Clock Work"):
    """
    Send email using Django templates with both HTML and plain text versions.
    This improves deliverability and reduces spam score.
    """
    if context is None:
        context = {}
    
    # Add common context variables
    context.update({
        'current_year': datetime.now().year,
        'user_email': to_email,
    })
    
    # Render HTML email from template
    html_content = render_to_string(f'emails/{template_name}.html', context)
    
    # Try to render plain text version, fallback to stripped HTML
    try:
        text_content = render_to_string(f'emails/{template_name}.txt', context)
    except:
        text_content = strip_tags(html_content)
    
    # Prepare Mailjet data with improved headers for deliverability
    data = {
        'Messages': [
            {
                "From": {
                    "Email": settings.MAIL_JET_EMAIL_ADDRESS,
                    "Name": from_name
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": to_email.split('@')[0].title()
                    }
                ],
                "Subject": subject,
                "TextPart": text_content,
                "HTMLPart": html_content,
                "CustomID": f"{to_email}_{int(time.time())}",
                "Headers": {
                    "Reply-To": settings.MY_EMAIL_ADDRESS,
                },
                # Add list unsubscribe header for better deliverability
                "CustomCampaign": "clock_work_notifications"
            }
        ]
    }
    
    try:
        result = mailjet.send.create(data=data)
        return result.status_code == 200
    except Exception as e:
        print(f"Error sending email to {to_email}: {str(e)}")
        return False


@shared_task(bind=True, name='clock_work.send_email_app.send_mail_func')
def send_mail_func(self):
    """Send welcome email to all users using professional template"""
    users = get_user_model().objects.all()
    for user in users:
        context = {
            'user_email': user.email,
        }
        send_email_with_template(
            to_email=user.email,
            subject="Welcome to Clock Work - Your Reminder & Notes Manager",
            template_name='welcome_email',
            context=context
        )
    return "Done"


@shared_task(bind=True, name='clock_work.send_email_app.send_mail_task')
def send_mail_task(self, emails, headline, content):
    """Send notification email to multiple recipients with progress tracking"""
    progress_recorder = ProgressRecorder(self)
    for email_no in range(len(emails)):
        context = {
            'headline': headline,
            'content': content,
            'subject': headline,
            'user_email': emails[email_no],
        }
        
        send_email_with_template(
            to_email=emails[email_no],
            subject=headline,
            template_name='notification_email',
            context=context
        )
        
        progress_recorder.set_progress(email_no + 1, len(emails), f'Sending notification to {emails[email_no]}')

    return "Done"


@shared_task(bind=True, name='clock_work.send_email_app.send_mail_task_with_schedule')
def send_mail_task_with_schedule(self, emails, headline, content):
    """Send scheduled notification email to multiple recipients"""
    for email_no in range(len(emails)):
        context = {
            'headline': headline,
            'content': content,
            'subject': headline,
            'user_email': emails[email_no],
        }
        
        send_email_with_template(
            to_email=emails[email_no],
            subject=headline,
            template_name='notification_email',
            context=context
        )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",
        {
            'type': 'send_notification',
            'message': json.dumps(f"Mail sent to {emails} with headline {headline}")
        }
    )
    return "Done"


@shared_task(bind=True, name='clock_work.send_email_app.ws_task')
def ws_task(self, number):
    progress_recorder = WebSocketProgressRecorder(self)
    for i in range(number):
        time.sleep(.1)
        progress_recorder.set_progress(i + 1, number)
    return int(random() * 1000)


@shared_task(bind=True, name='clock_work.send_email_app.web_socket_send_mail_task')
def web_socket_send_mail_task(self, emails, headline, content):
    """Send notification email via WebSocket with progress tracking"""
    progress_recorder = WebSocketProgressRecorder(self)
    for email_no in range(len(emails)):
        context = {
            'headline': headline,
            'content': content,
            'subject': headline,
            'user_email': emails[email_no],
        }
        
        send_email_with_template(
            to_email=emails[email_no],
            subject=headline,
            template_name='notification_email',
            context=context
        )
        
        progress_recorder.set_progress(email_no + 1, len(emails), f'Sending notification to {emails[email_no]}')

    return "Done"
