from django.shortcuts import render, get_object_or_404, redirect

from .models import Realization, Appointment
from .forms import AppointmentForm

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
    """Try to reserve an appointment"""
    if request.method != 'POST':
        # No data submitted
        form = AppointmentForm()
    else:
        # POST data submitted
        form = AppointmentForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('budowlanka_project:appointment')

    context = {'form': form}
    return render(request, 'mainapp/appointment.html', context)


def contact(request):
    """Contact page"""
    return render(request, 'mainapp/contact.html')
