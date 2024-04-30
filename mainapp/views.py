from django.shortcuts import render
from .models import Realization


def index(request):
    """The home page for Budowlanka"""
    return render(request, 'mainapp/index.html')


def blog(request):
    """Show all entries"""
    entries = Realization.objects.all()
    context = {'entries': entries}
    return render(request, 'mainapp/blog.html', context=context)


# def entry(request, entry_id):


def contact(request):
    """Contact page"""
    return render(request, 'mainapp/contact.html')
