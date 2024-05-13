from django.shortcuts import render, get_object_or_404

from .models import Realization, Appointment


def index(request):
    """The home page for Budowlanka"""
    return render(request, 'mainapp/index.html')


def blog(request):
    """Show all entries"""
    entries = Realization.objects.all()
    context = {'entries': entries}
    return render(request, 'mainapp/blog.html', context=context)


def detail(request, entry_id):
    # show entry and its comments
    entry = get_object_or_404(Realization, pk=entry_id)
    context = {'entry': entry, 'content': entry.content}
    return render(request, 'mainapp/detail.html', context)


def appointment(request):
    """Home page for appointments"""
    appointments = Appointment.objects.all()
    context = {'appointments': appointments}
    return render(request, 'mainapp/appointment.html', context)


def contact(request):
    """Contact page"""
    return render(request, 'mainapp/contact.html')
