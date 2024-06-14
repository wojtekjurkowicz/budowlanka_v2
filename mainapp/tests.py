from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse
from django.core.paginator import Page
from django.contrib.admin.sites import AdminSite

from .forms import AppointmentForm, CommentForm, ContactForm
from .models import Appointment, Realization, Comment
from .admin import RealizationAdmin, AppointmentAdmin, CommentAdmin
from .views import CalendarView


class AppointmentModelTest(TestCase):
    def test_str_representation(self):
        appointment = Appointment(description="Test Appointment", date="2024-05-21")
        self.assertEqual(str(appointment), "Test Appointment")


class RealizationModelTest(TestCase):
    def test_str_representation(self):
        realization = Realization(title="Test", content="Test Realization", date="2024-05-21")
        self.assertEqual(str(realization), "Test Realization...")


class CommentModelTest(TestCase):
    def test_str_representation(self):
        comment = Comment(realization_id=1, author_id=1, content="Test Comment", date="2024-05-21")
        self.assertEqual(str(comment), "Test Comment")


class AppointmentFormTest(TestCase):
    def test_valid_form(self):
        form = AppointmentForm(data={'description': 'Test Description', 'date': "2024-05-21"})
        self.assertTrue(form.is_valid())


class CommentFormTest(TestCase):
    def test_valid_form(self):
        form = CommentForm(data={'content': 'Test Content', 'date': "2024-05-21"})
        self.assertTrue(form.is_valid())


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('mainapp:blog')
        self.appointment_url = reverse('mainapp:appointment')
        self.contact_url = reverse('mainapp:contact')

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create a test realization and comment
        self.realization = Realization.objects.create(title="Test Title", content="Test Content")
        self.detail_url = reverse('mainapp:detail', args=[self.realization.id])
        self.client.login(username='testuser', password='password')

    def test_blog_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/blog.html')

    def test_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/detail.html')

    def test_appointment_view_get(self):
        response = self.client.get(self.appointment_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/appointment.html')

    def test_appointment_view_post(self):
        response = self.client.post(self.appointment_url, {
            'description': 'Test Appointment',
            'date': '2024-05-21T10:00:00Z'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful post

    def test_contact_view(self):
        # Symulacja wysłania formularza kontaktowego
        response = self.client.post(self.contact_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'message': 'Test message'
        })

        # Sprawdzenie czy nastąpiło przekierowanie
        self.assertRedirects(response, reverse('mainapp:index'), fetch_redirect_response=False)

        # Sprawdzenie czy po przekierowaniu jest status 200 na stronie głównej
        response = self.client.get(reverse('mainapp:index'))
        self.assertEqual(response.status_code, 200)

        # Sprawdzenie czy użyto odpowiedniego szablonu
        self.assertTemplateUsed(response, 'mainapp/index.html')

    def test_comment_creation(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.detail_url, {'content': 'New Test Comment', 'date': '2024-05-21'})
        self.assertEqual(response.status_code, 302)  # Should redirect after successful post
        self.assertEqual(Comment.objects.count(), 1)  # Ensure that the comment is created


class AppointmentEmailTest(TestCase):
    def setUp(self):
        # Utwórz użytkownika do autoryzacji
        self.user = User.objects.create_user(username='testuser', password='12345', email='testuser@example.com')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_appointment_email_sent(self):
        # Sprawdź początkowy stan mail.outbox
        self.assertEqual(len(mail.outbox), 0)

        # Wykonaj żądanie POST, aby utworzyć wizytę
        response = self.client.post(reverse('mainapp:appointment'), {
            'description': 'Testowa wizyta',
            'date': '2024-05-21T10:00:00Z'
        })

        # Sprawdź aktualny stan mail.outbox po wysłaniu e-maila
        self.assertEqual(len(mail.outbox), 1)

        # Sprawdź treść wysłanego e-maila
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Potwierdzenie wizyty')
        self.assertEqual(email.to, [self.user.email])
        self.assertIn('Testowa wizyta', email.body)


class TestPagination(TestCase):
    def setUp(self):
        # Tworzenie 15 realizacji
        for i in range(15):
            Realization.objects.create(title=f'Test Title {i}', content=f'Test Content {i}')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('mainapp:blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue(isinstance(response.context['page_obj'], Page))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_lists_all_realizations(self):
        # Sprawdzanie czy wszystkie realizacje są wyświetlane na stronie pierwszej
        response = self.client.get(reverse('mainapp:blog') + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_pagination_second_page(self):
        # Sprawdzanie czy druga strona zawiera pięć realizacji
        response = self.client.get(reverse('mainapp:blog') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(len(response.context['page_obj']), 5)


class MockRequest:
    pass


class AdminExportPDFTest(TestCase):
    def setUp(self):
        self.site = AdminSite()

        self.realization_admin = RealizationAdmin(Realization, self.site)
        self.appointment_admin = AppointmentAdmin(Appointment, self.site)
        self.comment_admin = CommentAdmin(Comment, self.site)

        self.realization = Realization.objects.create(title="Test Title", content="Test Content")
        self.appointment = Appointment.objects.create(description="Test Appointment", date="2024-05-21")
        self.comment = Comment.objects.create(realization=self.realization,
                                              author=User.objects.create(username='testuser'), content="Test Comment")

    def test_realization_export_to_pdf(self):
        queryset = Realization.objects.all()
        request = MockRequest()
        response = self.realization_admin.export_to_pdf(request, queryset)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename="database_report.pdf"', response['Content-Disposition'])

    def test_appointment_export_to_pdf(self):
        queryset = Appointment.objects.all()
        request = MockRequest()
        response = self.appointment_admin.export_to_pdf(request, queryset)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename="database_report.pdf"', response['Content-Disposition'])

    def test_comment_export_to_pdf(self):
        queryset = Comment.objects.all()
        request = MockRequest()
        response = self.comment_admin.export_to_pdf(request, queryset)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename="database_report.pdf"', response['Content-Disposition'])


class TestCalendarView(TestCase):
    def test_format_day_with_appointments(self):
        appointment = Appointment.objects.create(description="Test Appointment", date="2024-05-21")
        calendar = CalendarView()
        day_html = calendar.formatday(21, 1, Appointment.objects.all())
        self.assertIn('<span class=\'date\'>21</span>', day_html)
        self.assertIn('<li> Test Appointment </li>', day_html)

    def test_format_day_without_appointments(self):
        calendar = CalendarView()
        day_html = calendar.formatday(21, 1, Appointment.objects.none())
        self.assertIn('<span class=\'date\'>21</span>', day_html)
        self.assertNotIn('<li>', day_html)


class TestShowPDFView(TestCase):
    def test_show_pdf(self):
        response = self.client.get(reverse('mainapp:show_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename="hello.pdf"', response['Content-Disposition'])


class TestContactForm(TestCase):
    def test_contact_form_valid(self):
        form = ContactForm(
            data={'first_name': 'Test', 'last_name': 'User', 'email': 'test@example.com', 'message': 'Test Message'})
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid(self):
        form = ContactForm(data={'first_name': '', 'last_name': '', 'email': 'invalid', 'message': ''})
        self.assertFalse(form.is_valid())
