from django import forms
from .models import Appointment, Comment


# Form for creating and updating Appointment instances
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['description', 'date']  # Fields to be included in the form
        widgets = {
            'description': forms.Textarea(attrs={'placeholder':'Opis','style':'width: 300px','class': 'form-control'}),
            'date': forms.DateInput(attrs={'style':'width: 300px','class': 'form-control'}),
        }


# Form for creating and updating Comment instances
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Field to be included in the form
        widgets = {
            'content': forms.Textarea(attrs={'placeholder':'Treść komentarza','style':'width: 100%; height: 90px','class': 'form-control'})  # Customize the textarea widget with a CSS class
        }


# Simple contact form for collecting user messages
class ContactForm(forms.Form):
    #first_name = forms.CharField(label='Imię', max_length=100)  # Field for the first name
    #last_name = forms.CharField(label='Nazwisko', max_length=100)  # Field for the last name
    #email = forms.EmailField(label='Email')  # Field for the email address
    #message = forms.CharField(label='Treść wiadomości',
    #                         widget=forms.Textarea)  # Field for the message content with a textarea widget

    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder':'Imie','style':'width: 300px','class': 'form-control'}))  # Field for the first name
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder':'Nazwisko','style':'width: 300px','class': 'form-control'}))  # Field for the last name
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder':'Email','style':'width: 300px','class': 'form-control'}))  # Field for the email address
    message = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder':'Wiadomość','style':'width: 300px','class': 'form-control'}))  # Field for the message content with a textarea widget
