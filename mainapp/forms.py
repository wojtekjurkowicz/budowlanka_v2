from django import forms
from .models import Appointment, Comment, Message


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['description', 'date']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content', 'date']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
