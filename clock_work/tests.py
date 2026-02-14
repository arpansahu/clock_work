"""
Tests for clock_work main app
"""
from django.test import TestCase, Client
from django.urls import reverse
from clock_work import views


class ClockWorkViewsTest(TestCase):
    """Test main clock_work app views"""
    
    def setUp(self):
        self.client = Client()
    
    def test_home_view_exists(self):
        """Test that Home view is defined"""
        self.assertTrue(hasattr(views, 'Home'))
        self.assertTrue(hasattr(views.Home, 'as_view'))
    
    def test_celery_test_view_exists(self):
        """Test that CeleryTest view is defined"""
        self.assertTrue(hasattr(views, 'CeleryTest'))
        self.assertTrue(hasattr(views.CeleryTest, 'as_view'))
    
    def test_home_url_configured(self):
        """Test home URL is configured"""
        url = reverse('home')
        self.assertEqual(url, '/')
    
    def test_celery_test_url_configured(self):
        """Test celery test URL is configured"""
        url = reverse('test')
        self.assertEqual(url, '/test')


class ClockWorkURLsTest(TestCase):
    """Test main app URL configuration"""
    
    def test_home_url_resolves(self):
        """Test home URL resolves correctly"""
        url = reverse('home')
        self.assertEqual(url, '/')
    
    def test_test_url_resolves(self):
        """Test test URL resolves correctly"""
        url = reverse('test')
        self.assertEqual(url, '/test')
    
    def test_sendmail_to_all_url_resolves(self):
        """Test sendmailtoall URL resolves correctly"""
        url = reverse('sendmail_to_all')
        self.assertEqual(url, '/sendmailtoall/')
    
    def test_schedule_mail_url_resolves(self):
        """Test schedule_mail URL resolves correctly"""
        url = reverse('schedule_mail')
        self.assertEqual(url, '/schedule_mail/')
    
    def test_send_mail_url_resolves(self):
        """Test send_mail URL resolves correctly"""
        url = reverse('send_mail')
        self.assertEqual(url, '/send_mail/')
