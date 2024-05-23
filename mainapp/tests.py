from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Appointment, Message, Realization, Comment
from .forms import AppointmentForm, MessageForm, CommentForm


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
        self.assertTemplateUsed(response, 'mainapp/message.html')

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
        # Make a POST request to create an appointment
        response = self.client.post(reverse('mainapp:appointment'), {
            'description': 'Test appointment',
            'date': '2024-05-21T10:00:00Z'
        })

        # Check if the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Check if an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Verify the email subject and recipient
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Potwierdzenie wizyty')
        self.assertEqual(email.to, [self.user.email])
        self.assertIn('Test appointment', email.body)

