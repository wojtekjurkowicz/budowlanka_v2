from django import forms
from .models import Appointment, Comment, Message


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


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
