from asgiref.sync import sync_to_async
from django.http import HttpResponse
from django.shortcuts import render
from braces import views

# Create your views here.
from django.views import View
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from .tasks import send_mail_func, send_mail_task, ws_task
from celery_progress.backend import ProgressRecorder

class CelerySendMailToAll(View):
    def get(self, *args, **kwargs):
        send_mail_func.delay()
        return HttpResponse("Done")


class SendMail(views.JSONResponseMixin, views.AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        headline = request.POST.get('headline')
        emails = request.POST.get('emails').split(' ')
        content = request.POST.get('content')
        print(emails)
        try:
            # raise TypeError("Only integers are allowed")
            # send_mail_task.delay(emails, headline, content)
            task = send_mail_task.apply_async(args=[emails, headline, content])
            return self.render_json_response({"status": "Success", "message": "Notes Send", "task_id": task.task_id}, status = 200)
        except Exception as e:
            print("inside Exception")
            return self.render_json_response({"status": "Failed", "message": "Notes Can't be Sent"},  status=400)


class ScheduleMail(views.JSONResponseMixin, views.AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        headline = request.POST.get('')
        print(headline)
        try:
            schedule, created = CrontabSchedule.objects.get_or_create(hour=1, minute=57)
            task = PeriodicTask.objects.create(crontab=schedule, name="schedule_mail_task_"
                                                                      + str(len(PeriodicTask.objects.all())),
                                               task='send_email_app.tasks.send_mail_func',
                                               # args=json.dumps((2, 3))
                                               )
            return self.render_json_response({'status': 200, 'message': 'Reminder Scheduled'})
        except Exception as e:
            return self.render_json_response({'status': 400, 'message': "Reminder Can't be Scheduled"})


class WebSocketSendMail(views.JSONResponseMixin, views.AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        headline = request.POST.get('headline')
        emails = request.POST.get('emails').split(' ')
        content = request.POST.get('content')
        print(emails)
        try:
            # raise TypeError("Only integers are allowed")
            # send_mail_task.delay(emails, headline, content)
            task = send_mail_task.apply_async(args=[emails, headline, content])
            return self.render_json_response({"status": "Success", "message": "Notes Send", "task_id": task.task_id}, status = 200)
        except Exception as e:
            print("inside Exception")
            return self.render_json_response({"status": "Failed", "message": "Notes Can't be Sent"},  status=400)


def ws_view(request):
    result = ws_task.delay(number=100)
    return render(request, 'ws.html', context={'task_ids': [result.task_id]})