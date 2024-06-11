"""Defines URL patterns for accounts."""

from django.urls import path, include

from . import views

app_name = 'accounts'
urlpatterns = [
    # Registration page
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    # include default auth urls.
    path('', include('django.contrib.auth.urls')),
]
