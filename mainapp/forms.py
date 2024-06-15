from django import forms
from .models import Appointment, Comment


# Form for creating and updating Appointment instances
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['description', 'date']  # Fields to be included in the form


# Form for creating and updating Comment instances
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Field to be included in the form
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})  # Customize the textarea widget with a CSS class
        }


# Simple contact form for collecting user messages
class ContactForm(forms.Form):
    first_name = forms.CharField(label='Imię', max_length=100)  # Field for the first name
    last_name = forms.CharField(label='Nazwisko', max_length=100)  # Field for the last name
    email = forms.EmailField(label='Email')  # Field for the email address
    message = forms.CharField(label='Treść wiadomości',
                              widget=forms.Textarea)  # Field for the message content with a textarea widget
