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

from .forms import ContactForm
from .models import Realization, RealizationImage

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
    Show all entries and main image (if it exists).

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


@require_http_methods(["GET", "POST"])
def detail(request, entry_id):
    """
    Show entry, its comments and images.

    Args:
        request (HttpRequest): The request object.
        entry_id (int): The ID of the entry.

    Returns:
        HttpResponse: The rendered detail page of the entry.
    """
    try:
        entry = get_object_or_404(Realization, pk=entry_id)
        images = RealizationImage.objects.filter(realization=entry)

        context = {'entry': entry, 'images': images}
        logger.debug(f"Widok szczegółowy dla realizacji {entry_id}")
        return render(request, 'mainapp/detail.html', context)
    except Realization.DoesNotExist:
        logger.error(f"Realizacja o id {entry_id} nie istnieje")
        raise Http404("Podany wpis nie istnieje")
    except Exception as e:
        logger.error(f"Błąd w widoku szczegółowym dla realizacji {entry_id}: {e}")
        return render(request, 'mainapp/error.html', {'error': str(e)})


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
