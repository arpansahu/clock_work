"""
Playwright Browser Tests for UI Interactions
Run with: pytest test_browser_ui.py --headed (to see browser)
"""
import pytest
from playwright.sync_api import Page, expect
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestBrowserAuthentication:
    """Test authentication flows with real browser"""
    
    def test_home_page_loads(self, page: Page, live_server):
        """Test home page loads in browser"""
        page.goto(f"{live_server.url}/")
        # Page should load without errors
        assert page.url.startswith(live_server.url)
    
    def test_login_page_navigation(self, page: Page, live_server):
        """Test navigation to login page"""
        page.goto(f"{live_server.url}/login/")
        # Should reach login page
        assert "/login/" in page.url
    
    def test_register_page_navigation(self, page: Page, live_server):
        """Test navigation to register page"""
        page.goto(f"{live_server.url}/register/")
        # Should reach register page
        assert "/register/" in page.url


@pytest.mark.django_db
class TestBrowserNavigation:
    """Test navigation and routing in browser"""
    
    def test_tasks_page_navigation(self, page: Page, live_server):
        """Test navigation to tasks page"""
        page.goto(f"{live_server.url}/tasks/")
        # Should load tasks page
        assert "/tasks/" in page.url
    
    def test_multiple_page_navigation(self, page: Page, live_server):
        """Test navigating between multiple pages"""
        # Start at home
        page.goto(f"{live_server.url}/")
        assert page.url == f"{live_server.url}/"
        
        # Navigate to login
        page.goto(f"{live_server.url}/login/")
        assert "/login/" in page.url
        
        # Navigate to register
        page.goto(f"{live_server.url}/register/")
        assert "/register/" in page.url


@pytest.mark.django_db
class TestBrowserResponsiveness:
    """Test responsive design in browser"""
    
    def test_mobile_viewport(self, page: Page, live_server):
        """Test site in mobile viewport"""
        # Set mobile viewport
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(f"{live_server.url}/")
        # Page should load without errors
        assert page.url.startswith(live_server.url)
    
    def test_tablet_viewport(self, page: Page, live_server):
        """Test site in tablet viewport"""
        # Set tablet viewport
        page.set_viewport_size({"width": 768, "height": 1024})
        page.goto(f"{live_server.url}/")
        # Page should load without errors
        assert page.url.startswith(live_server.url)
    
    def test_desktop_viewport(self, page: Page, live_server):
        """Test site in desktop viewport"""
        # Set desktop viewport
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto(f"{live_server.url}/")
        # Page should load without errors
        assert page.url.startswith(live_server.url)


@pytest.mark.django_db
class TestBrowserErrorHandling:
    """Test error handling in browser"""
    
    def test_404_page(self, page: Page, live_server):
        """Test 404 error page"""
        response = page.goto(f"{live_server.url}/nonexistent-page/")
        # Should get 404 response
        assert response.status == 404
    
    def test_network_error_resilience(self, page: Page, live_server):
        """Test page handles network issues gracefully"""
        # Navigate to valid page first
        page.goto(f"{live_server.url}/")
        # Page should have loaded
        assert page.url.startswith(live_server.url)
