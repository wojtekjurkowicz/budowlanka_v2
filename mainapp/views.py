from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.utils.safestring import mark_safe
from django.utils import timezone

from calendar import HTMLCalendar
import logging

from .forms import AppointmentForm, CommentForm, MessageForm
from .models import Realization, Comment, Appointment

# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request):
    """The home page for Budowlanka"""
    try:
        logger.debug("Renderowanie strony głównej")
        return render(request, 'mainapp/index.html')
    except Exception as e:
        logger.error(f"Problem przy renderowaniu strony głównej: {e}")
        return render(request, 'mainapp/error.html', {'error': str(e)})


def blog(request):
    """Show all entries"""
    try:
        entries = Realization.objects.all()
        context = {'entries': entries}
        logger.debug("Pobrano wszystkie wpisy")
        return render(request, 'mainapp/blog.html', context=context)
    except Realization.DoesNotExist:
        logger.error("Żadne wpisy nie istnieją")
        raise Http404("Żaden wpis nie istnieje")
    except Exception as e:
        logger.error(f"Błąd podczas pobierania wpisów: {e}")
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
                logger.info(f"Nowy komentarz dodany przez {request.user} do realizacji {entry_id}")
                return redirect('mainapp:detail', entry_id=entry.id)
        else:
            comment_form = CommentForm()
        context = {'entry': entry, 'comments': comments, 'comment_form': comment_form}
        logger.debug(f"Widok szczegółowy dla realizacji {entry_id}")
        return render(request, 'mainapp/detail.html', context)
    except Realization.DoesNotExist:
        logger.error(f"Realizacja o id {entry_id} nie istnieje")
        raise Http404("Podany wpis nie istnieje")
    except Exception as e:
        logger.error(f"Błąd w widoku szczegółowym dla realizacji {entry_id}: {e}")
        return render(request, 'mainapp/error.html', {'error': str(e)})


@login_required
@require_http_methods(["GET", "POST"])
def message(request):
    """Message page"""
    try:
        if request.method != 'POST':
            # No data submitted
            form = MessageForm()
            logger.debug("Renderowanie formularza wiadomości")
        else:
            # POST data submitted
            form = MessageForm(data=request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.author = request.user
                message.save()
                logger.info(f"Wiadomość wysłana przez {request.user}")
                return redirect('mainapp:message')
            else:
                logger.error(f"Formularz wiadomości nie jest poprawny: {form.errors}")

        context = {'form': form}
        return render(request, 'mainapp/message.html', context)
    except Exception as e:
        logger.error(f"Błąd w widoku wiadomości: {e}")
        return render(request, 'mainapp/error.html', {'error': str(e)})


class CalendarView(HTMLCalendar):
    def formatday(self, day, weekday, appointments):
        """
        Return a day as a table cell.
        """
        appointments_per_day = appointments.filter(date__day=day)
        d = ''
        for appointment in appointments_per_day:
            d += f'<li> {appointment.description} </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, appointments):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, appointments) for (d, wd) in theweek)
        return f'<tr> {s} </tr>'

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        appointments = Appointment.objects.filter(date__year=theyear, date__month=themonth)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(theyear, themonth, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(theyear, themonth):
            cal += f'{self.formatweek(week, appointments)}\n'
        return cal


@require_http_methods(["GET", "POST"])
def appointment(request):
    """Try to reserve an appointment"""
    try:
        if request.method != 'POST':
            # No data submitted
            form = AppointmentForm()
            logger.debug("Renderowanie formularza wizyty")
        else:
            # POST data submitted
            form = AppointmentForm(data=request.POST)
            if form.is_valid():
                appointment = form.save()
                now = timezone.now()

                send_mail(
                    'Potwierdzenie wizyty',
                    f'Twoja wizyta została umówiona na {appointment.date}. Opis: {appointment.description}',
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=False,
                )
                logger.info(f"Wizyta utworzona na {appointment.date} z opisem {appointment.description}")
                return redirect('mainapp:appointment')
            else:
                logger.error(f"Formularz wizyty nie jest poprawny: {form.errors}")

        cal = CalendarView()
        now = timezone.now()
        html_cal = cal.formatmonth(now.year, now.month)

        context = {
            'form': form,
            'calendar': mark_safe(html_cal),
            'current_year': now.year,
            'current_month': now.month,
        }
        return render(request, 'mainapp/appointment.html', context)
    except Exception as e:
        logger.error(f"Błąd w widoku wizyty: {e}")
        return render(request, 'mainapp/error.html', {'error': str(e)})


def contact(request):
    """Contact page"""
    try:
        logger.debug("Renderowanie strony kontaktowej")
        return render(request, 'mainapp/contact.html')
    except Exception as e:
        logger.error(f"Błąd podczas renderowania strony kontaktowej: {e}")
        return render(request, 'mainapp/error.html', {'error': str(e)})
