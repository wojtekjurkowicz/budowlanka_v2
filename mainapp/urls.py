"""Defines URL patterns for budowlanka project"""

from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'budowlanka_project'
urlpatterns = [
    # Home page, cache for 15 minutes
    path('', cache_page(60 * 15)(views.index), name='index'),
    # Blog page, cache for 10 minutes
    path('blog/', cache_page(60 * 10)(views.blog), name='blog'),
    # Detail page for a single entry on blog, cache for 5 minutes
    path('blog/<int:entry_id>/', cache_page(60 * 5)(views.detail), name='detail'),
    # Appointments page, without cache
    path('umowwizyte/', views.appointment, name='appointment'),
    # Message page, without cache
    path('wiadomosc/', views.message, name='message'),
    # Contact page, without cache
    path('kontakt/', views.contact, name='contact'),
]
