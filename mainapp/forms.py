from django import forms
from .models import Appointment, Comment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['description', 'date']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }


class ContactForm(forms.Form):
    first_name = forms.CharField(label='Imię', max_length=100)
    last_name = forms.CharField(label='Nazwisko', max_length=100)
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Treść wiadomości', widget=forms.Textarea)
