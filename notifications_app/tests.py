"""
Tests for notifications_app
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from notifications_app.models import BroadcastNotification
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()


class BroadcastNotificationModelTest(TestCase):
    """Test BroadcastNotification model"""
    
    def setUp(self):
        self.broadcast_time = timezone.now() + timedelta(hours=1)
        self.notification = BroadcastNotification.objects.create(
            message='Test broadcast notification',
            broadcast_on=self.broadcast_time,
            sent=False
        )
    
    def test_notification_creation(self):
        """Test creating a broadcast notification"""
        self.assertIsInstance(self.notification, BroadcastNotification)
        self.assertEqual(self.notification.message, 'Test broadcast notification')
        self.assertFalse(self.notification.sent)
    
    def test_notification_str(self):
        """Test notification has message attribute"""
        self.assertTrue(hasattr(self.notification, 'message'))
        self.assertEqual(self.notification.message, 'Test broadcast notification')
    
    def test_notification_ordering(self):
        """Test notifications are ordered by broadcast_on descending"""
        notification2 = BroadcastNotification.objects.create(
            message='Second notification',
            broadcast_on=timezone.now() + timedelta(hours=2),
            sent=False
        )
        
        notifications = BroadcastNotification.objects.all()
        # Should be ordered by broadcast_on descending
        self.assertEqual(notifications[0], notification2)
        self.assertEqual(notifications[1], self.notification)


class NotificationViewTest(TestCase):
    """Test notifications_app views"""
    
    def setUp(self):
        self.client = Client()
    
    def test_notification_test_view_url_exists(self):
        """Test that notification test view URL exists"""
        url = reverse('test_notification')
        self.assertEqual(url, '/test/notification/')


class NotificationURLsTest(TestCase):
    """Test notification URLs"""
    
    def test_test_notification_url_resolves(self):
        """Test test_notification URL resolves correctly"""
        url = reverse('test_notification')
        self.assertEqual(url, '/test/notification/')
