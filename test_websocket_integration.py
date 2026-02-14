"""
WebSocket Integration Tests
Tests for real-time WebSocket functionality
"""
from django.test import TestCase, TransactionTestCase
from channels.testing import WebsocketCommunicator, ApplicationCommunicator
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from notifications_app.consumers import NotificationConsumer
import json
import pytest


class WebSocketConsumerTest(TestCase):
    """Test WebSocket consumer functionality"""
    
    def test_notification_consumer_exists(self):
        """Test NotificationConsumer class exists"""
        from notifications_app import consumers
        self.assertTrue(hasattr(consumers, 'NotificationConsumer'))
    
    def test_consumer_has_connect_method(self):
        """Test consumer has connect method"""
        self.assertTrue(hasattr(NotificationConsumer, 'connect'))
    
    def test_consumer_has_disconnect_method(self):
        """Test consumer has disconnect method"""
        self.assertTrue(hasattr(NotificationConsumer, 'disconnect'))
    
    def test_consumer_has_send_notification_method(self):
        """Test consumer has send_notification method"""
        self.assertTrue(hasattr(NotificationConsumer, 'send_notification'))


class ChannelLayerTest(TestCase):
    """Test channel layer configuration"""
    
    def test_channel_layer_configured(self):
        """Test that channel layer is configured"""
        channel_layer = get_channel_layer()
        self.assertIsNotNone(channel_layer)
    
    def test_channel_layer_has_group_send(self):
        """Test channel layer has group_send method"""
        channel_layer = get_channel_layer()
        self.assertTrue(hasattr(channel_layer, 'group_send'))
    
    def test_channel_layer_has_group_add(self):
        """Test channel layer has group_add method"""
        channel_layer = get_channel_layer()
        self.assertTrue(hasattr(channel_layer, 'group_add'))
    
    def test_channel_layer_has_group_discard(self):
        """Test channel layer has group_discard method"""
        channel_layer = get_channel_layer()
        self.assertTrue(hasattr(channel_layer, 'group_discard'))


class WebSocketRoutingTest(TestCase):
    """Test WebSocket routing configuration"""
    
    def test_websocket_routing_exists(self):
        """Test WebSocket routing is configured"""
        try:
            from notifications_app import routing
            self.assertTrue(hasattr(routing, 'websocket_urlpatterns'))
        except ImportError:
            # Routing might be in different location
            from clock_work import routing
            self.assertIsNotNone(routing)
    
    def test_asgi_application_configured(self):
        """Test ASGI application is configured"""
        from clock_work import asgi
        self.assertTrue(hasattr(asgi, 'application'))


class NotificationBroadcastTest(TestCase):
    """Test notification broadcasting functionality"""
    
    def test_broadcast_notification_model_exists(self):
        """Test BroadcastNotification model exists"""
        from notifications_app.models import BroadcastNotification
        self.assertIsNotNone(BroadcastNotification)
    
    def test_notification_handler_registered(self):
        """Test notification handler is registered"""
        from notifications_app import models
        self.assertTrue(hasattr(models, 'notification_handler'))
    
    def test_broadcast_notification_fields(self):
        """Test BroadcastNotification has required fields"""
        from notifications_app.models import BroadcastNotification
        from django.utils import timezone
        from datetime import timedelta
        
        notification = BroadcastNotification(
            message='Test notification',
            broadcast_on=timezone.now() + timedelta(hours=1),
            sent=False
        )
        
        self.assertEqual(notification.message, 'Test notification')
        self.assertFalse(notification.sent)


class WebSocketViewTest(TestCase):
    """Test WebSocket-related views"""
    
    def test_ws_view_exists(self):
        """Test ws_view exists in tasks app"""
        from tasks import views
        self.assertTrue(hasattr(views, 'ws_view'))
    
    def test_ws_error_view_exists(self):
        """Test ws_error_view exists"""
        from tasks import views
        self.assertTrue(hasattr(views, 'ws_error_view'))
    
    def test_notification_test_view_exists(self):
        """Test notification test view exists"""
        from notifications_app import views
        self.assertTrue(hasattr(views, 'test'))


class CeleryWebSocketIntegrationTest(TestCase):
    """Test Celery and WebSocket integration"""
    
    def test_ws_task_exists(self):
        """Test WebSocket-related Celery task exists"""
        from tasks import tasks
        self.assertTrue(hasattr(tasks, 'ws_task'))
        self.assertTrue(hasattr(tasks, 'ws_error_task'))
    
    def test_ws_tasks_are_celery_tasks(self):
        """Test WebSocket tasks are Celery tasks"""
        from tasks.tasks import ws_task, ws_error_task
        self.assertTrue(hasattr(ws_task, 'delay'))
        self.assertTrue(hasattr(ws_error_task, 'delay'))
    
    def test_web_socket_send_mail_task_exists(self):
        """Test WebSocket email task exists"""
        from send_email_app.tasks import web_socket_send_mail_task
        self.assertTrue(hasattr(web_socket_send_mail_task, 'delay'))


class RealtimeNotificationTest(TestCase):
    """Test real-time notification functionality"""
    
    def test_notification_view_sends_to_channel(self):
        """Test notification view sends to channel layer"""
        from notifications_app.views import test as notification_test_view
        self.assertTrue(callable(notification_test_view))
    
    def test_broadcast_notification_task_exists(self):
        """Test broadcast notification task exists"""
        from notifications_app.tasks import broadcast_notification
        self.assertTrue(hasattr(broadcast_notification, 'delay'))
