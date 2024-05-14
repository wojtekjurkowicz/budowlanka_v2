from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AppointmentForm, CommentForm, MessageForm
from .models import Realization, Comment


def index(request):
    """The home page for Budowlanka"""
    return render(request, 'mainapp/index.html')


def blog(request):
    """Show all entries"""
    entries = Realization.objects.all()
    context = {'entries': entries}
    return render(request, 'mainapp/blog.html', context=context)


@login_required
def detail(request, entry_id):
    # show entry and its comments
    entry = get_object_or_404(Realization, pk=entry_id)
    comments = Comment.objects.filter(realization=entry)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.realization = entry
            comment.save()
            return redirect('mainapp:detail', entry_id=entry.id)
    else:
        comment_form = CommentForm()
    context = {'entry': entry, 'comments': comments, 'comment_form': comment_form}
    return render(request, 'mainapp/detail.html', context)


@login_required
def message(request):
    """Message page"""
    if request.method != 'POST':
        # No data submitted
        form = MessageForm()
    else:
        # POST data submitted
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.save()
            return redirect('mainapp:message')

    context = {'form': form}
    return render(request, 'mainapp/message.html', context)


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
