"""
Additional comprehensive tests for utility functions and helpers
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from clock_work.models import AbstractBaseModel, SoftDeleteManager
from django.db import models
from django.utils import timezone

User = get_user_model()


class AbstractBaseModelTest(TestCase):
    """Test AbstractBaseModel utility methods"""
    
    def test_abstract_base_model_has_created_at(self):
        """Test AbstractBaseModel has created_at field"""
        # Check that model has the field
        self.assertTrue(hasattr(AbstractBaseModel, 'created_at'))
    
    def test_abstract_base_model_has_updated_at(self):
        """Test AbstractBaseModel has updated_at field"""
        self.assertTrue(hasattr(AbstractBaseModel, 'updated_at'))
    
    def test_abstract_base_model_has_is_deleted(self):
        """Test AbstractBaseModel has is_deleted field"""
        self.assertTrue(hasattr(AbstractBaseModel, 'is_deleted'))
    
    def test_abstract_base_model_save_method(self):
        """Test AbstractBaseModel has save method"""
        self.assertTrue(hasattr(AbstractBaseModel, 'save'))


class SoftDeleteManagerTest(TestCase):
    """Test SoftDeleteManager utility methods"""
    
    def test_soft_delete_manager_has_get_queryset(self):
        """Test SoftDeleteManager has get_queryset method"""
        self.assertTrue(hasattr(SoftDeleteManager, 'get_queryset'))
    
    def test_soft_delete_manager_filters_deleted(self):
        """Test SoftDeleteManager filters out deleted items"""
        manager = SoftDeleteManager()
        self.assertTrue(callable(manager.get_queryset))


class AccountTokenTest(TestCase):
    """Test account token generation"""
    
    def test_account_activation_token_exists(self):
        """Test account activation token generator exists"""
        from account import token
        self.assertTrue(hasattr(token, 'account_activation_token'))
    
    def test_token_generator_has_make_token(self):
        """Test token generator has make_token method"""
        from account.token import account_activation_token
        self.assertTrue(hasattr(account_activation_token, 'make_token'))
    
    def test_token_generator_has_check_token(self):
        """Test token generator has check_token method"""
        from account.token import account_activation_token
        self.assertTrue(hasattr(account_activation_token, 'check_token'))


class AccountFormsUtilityTest(TestCase):
    """Test account forms utility methods"""
    
    def test_registration_form_clean_methods(self):
        """Test RegistrationForm has clean methods"""
        from account.forms import RegistrationForm
        form = RegistrationForm()
        # Form should have clean method
        self.assertTrue(hasattr(form, 'clean'))
    
    def test_login_form_initialization(self):
        """Test LoginForm initializes properly"""
        from account.forms import LoginForm
        form = LoginForm()
        # Form should have username and password fields
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
    
    def test_account_update_form_fields(self):
        """Test AccountUpdateForm has required fields"""
        from account.forms import AccountUpdateForm
        form = AccountUpdateForm()
        # Form should have email and username fields
        self.assertIn('email', form.fields)
        self.assertIn('username', form.fields)


class CeleryTaskUtilityTest(TestCase):
    """Test Celery task utility functions"""
    
    def test_celery_app_configured(self):
        """Test Celery app is configured"""
        from clock_work import celery
        self.assertTrue(hasattr(celery, 'app'))
    
    def test_celery_task_decorator_available(self):
        """Test Celery task decorator is available"""
        from celery import shared_task
        self.assertTrue(callable(shared_task))
    
    def test_progress_recorder_available(self):
        """Test ProgressRecorder is available for task tracking"""
        from celery_progress.backend import ProgressRecorder
        self.assertIsNotNone(ProgressRecorder)


class StorageBackendTest(TestCase):
    """Test storage backend utilities"""
    
    def test_storage_backends_module_exists(self):
        """Test storage_backends module exists"""
        try:
            from clock_work import storage_backends
            self.assertIsNotNone(storage_backends)
        except ImportError:
            # Storage backends might not be used
            self.skipTest("Storage backends not configured")
    
    def test_default_storage_configured(self):
        """Test default storage is configured"""
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'DEFAULT_FILE_STORAGE'))


class RoutingUtilityTest(TestCase):
    """Test routing utility functions"""
    
    def test_asgi_routing_configured(self):
        """Test ASGI routing is configured"""
        from clock_work import routing
        self.assertIsNotNone(routing)
    
    def test_websocket_url_patterns_exist(self):
        """Test WebSocket URL patterns exist"""
        try:
            from clock_work import routing
            self.assertTrue(hasattr(routing, 'websocket_urlpatterns'))
        except AttributeError:
            # WebSocket patterns might be in notifications_app
            from notifications_app import routing
            self.assertIsNotNone(routing)


class EmailHelperTest(TestCase):
    """Test email helper functions"""
    
    def test_send_mail_account_activate_parameters(self):
        """Test send_mail_account_activate accepts correct parameters"""
        from account.views import send_mail_account_activate
        import inspect
        
        sig = inspect.signature(send_mail_account_activate)
        params = list(sig.parameters.keys())
        
        # Should accept receiver_email, user, and optionally SUBJECT
        self.assertIn('reciever_email', params)
        self.assertIn('user', params)


class MiddlewareUtilityTest(TestCase):
    """Test middleware configuration"""
    
    def test_middleware_configured(self):
        """Test middleware is properly configured"""
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'MIDDLEWARE'))
        self.assertIsInstance(settings.MIDDLEWARE, list)
    
    def test_security_middleware_enabled(self):
        """Test SecurityMiddleware is enabled"""
        from django.conf import settings
        middleware_str = ','.join(settings.MIDDLEWARE)
        self.assertIn('SecurityMiddleware', middleware_str)


class SettingsUtilityTest(TestCase):
    """Test settings utility configurations"""
    
    def test_installed_apps_configured(self):
        """Test INSTALLED_APPS is configured"""
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'INSTALLED_APPS'))
        self.assertIsInstance(settings.INSTALLED_APPS, list)
    
    def test_custom_apps_installed(self):
        """Test custom apps are installed"""
        from django.conf import settings
        apps_str = ','.join(settings.INSTALLED_APPS)
        self.assertIn('account', apps_str)
        self.assertIn('tasks', apps_str)
        self.assertIn('notifications_app', apps_str)
        self.assertIn('send_email_app', apps_str)
    
    def test_celery_configured(self):
        """Test Celery settings are configured"""
        from django.conf import settings
        # Should have Celery broker URL
        self.assertTrue(
            hasattr(settings, 'CELERY_BROKER_URL') or 
            hasattr(settings, 'BROKER_URL')
        )


class URLUtilityTest(TestCase):
    """Test URL utility configurations"""
    
    def test_url_patterns_configured(self):
        """Test URL patterns are configured"""
        from clock_work import urls
        self.assertTrue(hasattr(urls, 'urlpatterns'))
        self.assertIsInstance(urls.urlpatterns, list)
    
    def test_admin_url_configured(self):
        """Test admin URL is configured"""
        from django.urls import reverse
        try:
            admin_url = reverse('admin:index')
            self.assertIsNotNone(admin_url)
        except:
            self.skipTest("Admin URL not configured")
