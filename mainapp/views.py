import logging
import io
from calendar import HTMLCalendar

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.contrib import messages

from .forms import AppointmentForm, CommentForm, ContactForm
from .models import Realization, Comment, Appointment

# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request):
    """
    Render the home page for Budowlanka.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    try:
        logger.debug("Renderowanie strony głównej")
        return render(request, 'mainapp/index.html')
    except Exception as e:
        logger.error(f"Problem przy renderowaniu strony głównej: {e}")
        return render(request, 'mainapp/error.html', {'error': str(e)})


def blog(request):
    """
    Show all entries.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    try:
        entries = Realization.objects.all()
        paginator = Paginator(entries, 10)  # Paginate with 10 entries per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        logger.debug("Pobrano część wpisów")
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
    """
    Show entry and its comments.

    :param request: HttpRequest object.
    :param entry_id: ID of the entry.
    :return: HttpResponse object.
    """
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


class CalendarView(HTMLCalendar):
    def formatday(self, day, weekday, appointments):
        """
        Return a day as a table cell.

        :param day: The day number.
        :param weekday: The weekday number (0-6).
        :param appointments: QuerySet of appointments for the given day.
        :return: HTML representation of the day's cell.
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

        :param theweek: List of tuples containing (day, weekday) for the week.
        :param appointments: QuerySet of appointments for the given week.
        :return: HTML representation of the week's row.
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
    """
    Try to reserve an appointment.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    try:
        if request.method != 'POST':
            # No data submitted
            form = AppointmentForm()
            logger.debug("Renderowanie formularza wizyty")
        else:
            # POST data submitted
            form = AppointmentForm(data=request.POST)
            if form.is_valid():
                # Form is valid, process the data
                appointment = form.save()
                now = timezone.now()

                send_mail(
                    'Potwierdzenie wizyty',
                    f'Twoja wizyta została umówiona na {appointment.date}. Opis: {appointment.description}',
                    "wojtek.jurkowicz@gmail.com"
                    [request.user.email],
                    fail_silently=False,
                )
                logger.info("Wysłano e-mail potwierdzający wizytę.")
                logger.info(f"Wizyta utworzona na {appointment.date} z opisem {appointment.description}")
                # Always redirect back to the appointment page after a successful submission
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


@login_required
@require_http_methods(["GET", "POST"])
def contact(request):
    """
    Contact page.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    try:
        if request.method != 'POST':
            # No data submitted
            form = ContactForm()
            logger.debug("Renderowanie formularza kontaktowego")
        else:
            # POST data submitted
            form = ContactForm(data=request.POST)
            if form.is_valid():
                # przetwarzanie danych z formularza
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']

                send_mail(
                    f'Wiadomość od {first_name} {last_name}',
                    message,
                    email,
                    ['wojtek.jurkowicz@gmail.com'],
                    fail_silently=False,
                )

                messages.success(request, "Wiadomość została wysłana.")
                logger.info(f"Wiadomość wysłana przez {request.user}")
                return redirect('mainapp:index')
            else:
                logger.error(f"Formularz wiadomości nie jest poprawny: {form.errors}")

        context = {'form': form}
        return render(request, 'mainapp/contact.html', context)
    except Exception as e:
        logger.error(f"Błąd w widoku wiadomości: {e}")
        return render(request, 'mainapp/error.html', {'error': str(e)})


def show_pdf(request):
    """
    Display a PDF file.

    :param request: HttpRequest object.
    :return: FileResponse object.
    """
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 100, "Hello world.")
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")
