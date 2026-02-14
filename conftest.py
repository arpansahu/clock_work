"""
Pytest configuration for UI tests
"""
import pytest
from django.conf import settings


@pytest.fixture(scope="session")
def django_db_setup():
    """Configure Django database for pytest"""
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }


@pytest.fixture(scope="session")
def live_server_url():
    """Provide base URL for live server"""
    return "http://localhost:8000"
