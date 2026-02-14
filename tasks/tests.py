"""
Tests for tasks app (HTTP/WebSocket demo views)
"""
from django.test import TestCase, Client
from django.urls import reverse


class TasksViewTest(TestCase):
    """Test tasks views for HTTP/WebSocket demos"""
    
    def setUp(self):
        self.client = Client()
    
    def test_index_view(self):
        """Test index view"""
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_http_view(self):
        """Test HTTP view"""
        url = reverse('http')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'http.html')
    
    def test_http_error_view(self):
        """Test HTTP error view - expects StopIteration error"""
        url = reverse('http_error')
        with self.assertRaises(StopIteration):
            response = self.client.get(url)
    
    def test_ws_view(self):
        """Test WebSocket view"""
        url = reverse('ws')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ws.html')
    
    def test_ws_error_view(self):
        """Test WebSocket error view - expects StopIteration error"""
        url = reverse('ws_error')
        with self.assertRaises(StopIteration):
            response = self.client.get(url)


class TasksURLsTest(TestCase):
    """Test tasks URLs"""
    
    def test_index_url_resolves(self):
        """Test index URL resolves correctly"""
        url = reverse('index')
        self.assertTrue(url.startswith('/tasks/'))
    
    def test_http_url_resolves(self):
        """Test HTTP URL resolves correctly"""
        url = reverse('http')
        self.assertTrue(url.startswith('/tasks/'))
    
    def test_http_error_url_resolves(self):
        """Test HTTP error URL resolves correctly"""
        url = reverse('http_error')
        self.assertTrue(url.startswith('/tasks/'))
    
    def test_ws_url_resolves(self):
        """Test WebSocket URL resolves correctly"""
        url = reverse('ws')
        self.assertTrue(url.startswith('/tasks/'))
    
    def test_ws_error_url_resolves(self):
        """Test WebSocket error URL resolves correctly"""
        url = reverse('ws_error')
        self.assertTrue(url.startswith('/tasks/'))
