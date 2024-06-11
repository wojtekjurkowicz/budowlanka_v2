from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse
from django.core.paginator import Page

from .forms import AppointmentForm, MessageForm, CommentForm
from .models import Appointment, Message, Realization, Comment


class AppointmentModelTest(TestCase):
    def test_str_representation(self):
        appointment = Appointment(description="Test Appointment", date="2024-05-21")
        self.assertEqual(str(appointment), "Test Appointment")


class MessageModelTest(TestCase):
    def test_str_representation(self):
        message = Message(author_id=1, content="Test Message")
        self.assertEqual(str(message), "Test Message")


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


class MessageFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_valid_form(self):
        form = MessageForm(data={'content': 'Test Message'})
        message = form.save(commit=False)
        message.author = self.user
        self.assertTrue(form.is_valid())


class CommentFormTest(TestCase):
    def test_valid_form(self):
        form = CommentForm(data={'content': 'Test Content', 'date': "2024-05-21"})
        self.assertTrue(form.is_valid())


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('mainapp:blog')
        self.message_url = reverse('mainapp:message')
        self.appointment_url = reverse('mainapp:appointment')
        self.contact_url = reverse('mainapp:contact')

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create a test realization and comment
        self.realization = Realization.objects.create(title="Test Title", content="Test Content")
        self.detail_url = reverse('mainapp:detail', args=[self.realization.id])

    def test_blog_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/blog.html')

    def test_detail_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/detail.html')

    def test_message_view_get(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.message_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/contact.html')

    def test_message_view_post(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.message_url, {'content': 'Test Message'})
        self.assertEqual(response.status_code, 302)  # Should redirect after successful post

    def test_appointment_view_get(self):
        response = self.client.get(self.appointment_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/appointment.html')

    def test_appointment_view_post(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.appointment_url, {
            'description': 'Test Appointment',
            'date': '2024-05-21T10:00:00Z'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful post

    def test_contact_view(self):
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/contact.html')

    def test_comment_creation(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.detail_url, {'content': 'New Test Comment', 'date': '2024-05-21'})
        self.assertEqual(response.status_code, 302)  # Should redirect after successful post
        self.assertEqual(Comment.objects.count(), 1)  # Ensure that the comment is created


class AppointmentEmailTest(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='12345', email='testuser@example.com')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_appointment_email_sent(self):
        # Print the current state of mail.outbox
        print("mail.outbox before sending email:", mail.outbox)

        # Make a POST request to create an appointment
        response = self.client.post(reverse('budowlanka_project:appointment'), {
            'description': 'Test appointment',
            'data': '2024-05-21T10:00:00Z'
        })

        # Print the current state of mail.outbox after sending email
        print("mail.outbox after sending email:", mail.outbox)

        # Check if an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Verify the email subject and recipient
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Potwierdzenie wizyty')
        self.assertEqual(email.to, [self.user.email])
        self.assertIn('Test appointment', email.body)


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
