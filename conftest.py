"""
Pytest configuration for UI tests
"""
import pytest
from django.conf import settingsfrom playwright.sync_api import Browser


@pytest.fixture(scope="session")
def context(browser: Browser):
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture
def page(context):
    page = context.new_page()
    page.set_default_timeout(60000)
    page.set_default_navigation_timeout(60000)
    yield page
    page.close()

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
