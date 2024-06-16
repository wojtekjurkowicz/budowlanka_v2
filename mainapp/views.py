import logging
from calendar import HTMLCalendar

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods

from .forms import AppointmentForm, CommentForm, ContactForm
from .models import Realization, Comment, Appointment

# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request):
    """
    Render the home page for Budowlanka.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered home page.
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

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered blog page with paginated entries.
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

    Args:
        request (HttpRequest): The request object.
        entry_id (int): The ID of the entry.

    Returns:
        HttpResponse: The rendered detail page of the entry.
    """
    try:
        entry = get_object_or_404(Realization, pk=entry_id)
        comments = Comment.objects.filter(realization=entry)  # Get comments related to the realization

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                # Save comment with author and related realization
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
    """
    A class to represent a monthly calendar with appointments.
    """

    def formatday(self, day, weekday, appointments):
        """
        Return a day as a table cell.

        Args:
            day (int): The day number.
            weekday (int): The weekday number (0-6).
            appointments (QuerySet): QuerySet of appointments for the given day.

        Returns:
            str: HTML representation of the day's cell.
        """
        appointments_per_day = appointments.filter(date__day=day)
        d = ''.join(f'<li> Zajęty termin</li>' for appointment in appointments_per_day)  # {appointment.description}
        return f"<td><span class='date'>{day}</span><ul style='list-style-type:none;'> {d} </ul></td>" if day != 0 else '<td></td>'

    def formatweek(self, theweek, appointments):
        """
        Return a complete week as a table row.

        Args:
            theweek (list): List of tuples containing (day, weekday) for the week.
            appointments (QuerySet): QuerySet of appointments for the given week.

        Returns:
            str: HTML representation of the week's row.
        """
        return f'<tr> {" ".join(self.formatday(d, wd, appointments) for (d, wd) in theweek)} </tr>'

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.

        Args:
            theyear (int): The year of the month.
            themonth (int): The month to format.
            withyear (bool): Whether to include the year in the month name.

        Returns:
            str: HTML representation of the month's table.
        """
        appointments = Appointment.objects.filter(date__year=theyear, date__month=themonth)
        return ''.join([
            f'<table class="table table-bordered">\n',
            f'{self.formatmonthname(theyear, themonth, withyear=withyear)}\n',
            f'{self.formatweekheader()}\n',
            ''.join(self.formatweek(week, appointments) for week in self.monthdays2calendar(theyear, themonth)),
            '\n</table>'
        ])


@require_http_methods(["GET", "POST"])
def appointment(request):
    """
    Try to reserve an appointment.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered appointment page.
    """
    try:
        if request.method == 'POST':
            # POST data submitted
            form = AppointmentForm(data=request.POST)
            logger.debug(f"Data submitted: {request.POST}")
            if form.is_valid():
                # Form is valid, process the data
                appointment = form.save()

                send_mail(
                    'Potwierdzenie wizyty',
                    f'Twoja wizyta została umówiona na {appointment.day}-{appointment.month}-{appointment.year}. Opis: {appointment.description}',
                    "wojtek.jurkowicz@gmail.com",
                    [request.user.email],
                    fail_silently=False,
                )
                logger.info(f"Wizyta utworzona na {appointment.day}-{appointment.month}-{appointment.year} z opisem {appointment.description}")
                logger.info("Wysłano e-mail potwierdzający wizytę.")
                # Always redirect back to the appointment page after a successful submission
                return redirect('mainapp:appointment')
            else:
                logger.error(f"Formularz wizyty nie jest poprawny: {form.errors}")
        else:
            # No data submitted
            form = AppointmentForm()
            logger.debug("Renderowanie formularza wizyty")

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
    Render the contact page and handle form submission.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered contact page.
    """
    try:
        if request.method == 'POST':
            # POST data submitted
            form = ContactForm(data=request.POST)
            if form.is_valid():
                # Form is valid; process the data
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
        else:
            # No data submitted
            form = ContactForm()
            logger.debug("Renderowanie formularza kontaktowego")

        context = {'form': form}
        return render(request, 'mainapp/contact.html', context)
    except Exception as e:
        logger.error(f"Błąd w widoku wiadomości: {e}")
        return render(request, 'mainapp/error.html', {'error': str(e)})
