"""
URL Configuration for account app
"""
from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
