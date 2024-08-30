"""Defines URL patterns for budowlanka_v2 project"""

from django.urls import path

from . import views

app_name = 'budowlanka_project'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # Blog page
    path('blog/', views.blog, name='blog'),

    # Detail page for a single entry on blog
    path('blog/<int:entry_id>/', views.detail, name='detail'),

    # Contact page
    path('kontakt/', views.contact, name='contact'),
]
