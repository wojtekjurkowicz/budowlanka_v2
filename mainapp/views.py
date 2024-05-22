from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from .forms import AppointmentForm, CommentForm, MessageForm
from .models import Realization, Comment


def index(request):
    """The home page for Budowlanka"""
    try:
        return render(request, 'mainapp/index.html')
    except Exception as e:
        return render(request, 'mainapp/error.html', {'error': str(e)})


def blog(request):
    """Show all entries"""
    try:
        entries = Realization.objects.all()
        context = {'entries': entries}
        return render(request, 'mainapp/blog.html', context=context)
    except Realization.DoesNotExist:
        raise Http404("Żaden wpis nie istnieje")
    except Exception as e:
        return render(request, 'mainapp/error.html', {'error': str(e)})


@login_required
@require_http_methods(["GET", "POST"])
def detail(request, entry_id):
    # show entry and its comments
    try:
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
    except Realization.DoesNotExist:
        raise Http404("Podany wpis nie istnieje")
    except Exception as e:
        return render(request, 'mainapp/error.html', {'error': str(e)})


@login_required
@require_http_methods(["GET", "POST"])
def message(request):
    """Message page"""
    try:
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
    except Exception as e:
        return render(request, 'mainapp/error.html', {'error': str(e)})


@require_http_methods(["GET", "POST"])
def appointment(request):
    """Try to reserve an appointment"""
    try:
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
    except Exception as e:
        return render(request, 'mainapp/error.html', {'error': str(e)})


def contact(request):
    """Contact page"""
    try:
        return render(request, 'mainapp/contact.html')
    except Exception as e:
        return render(request, 'mainapp/error.html', {'error': str(e)})
