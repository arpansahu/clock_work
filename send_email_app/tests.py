"""
Tests for send_email_app
"""
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from send_email_app import views
from unittest.mock import patch, MagicMock
import json

User = get_user_model()


class SendEmailAppViewsTest(TestCase):
    """Test send_email_app views"""
    
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.user.is_active = True
        self.user.save()
    
    def test_send_mail_view_exists(self):
        """Test that SendMail view is defined"""
        self.assertTrue(hasattr(views, 'SendMail'))
        self.assertTrue(hasattr(views.SendMail, 'as_view'))
    
    def test_schedule_mail_view_exists(self):
        """Test that ScheduleMail view is defined"""
        self.assertTrue(hasattr(views, 'ScheduleMail'))
        self.assertTrue(hasattr(views.ScheduleMail, 'as_view'))
    
    def test_celery_send_mail_to_all_view_exists(self):
        """Test that CelerySendMailToAll view is defined"""
        self.assertTrue(hasattr(views, 'CelerySendMailToAll'))
        self.assertTrue(hasattr(views.CelerySendMailToAll, 'as_view'))
    
    def test_websocket_send_mail_view_exists(self):
        """Test that WebSocketSendMail view is defined"""
        self.assertTrue(hasattr(views, 'WebSocketSendMail'))
        self.assertTrue(hasattr(views.WebSocketSendMail, 'as_view'))
    
    def test_ws_view_function_exists(self):
        """Test that ws_view function is defined"""
        self.assertTrue(hasattr(views, 'ws_view'))
        self.assertTrue(callable(views.ws_view))


class SendEmailAppURLTest(TestCase):
    """Test send_email_app URL configuration"""
    
    def test_send_mail_url_exists(self):
        """Test send_mail URL is configured"""
        url = reverse('send_mail')
        self.assertEqual(url, '/send_mail/')
    
    def test_schedule_mail_url_exists(self):
        """Test schedule_mail URL is configured"""
        url = reverse('schedule_mail')
        self.assertEqual(url, '/schedule_mail/')
    
    def test_sendmail_to_all_url_exists(self):
        """Test sendmail_to_all URL is configured"""
        url = reverse('sendmail_to_all')
        self.assertEqual(url, '/sendmailtoall/')
