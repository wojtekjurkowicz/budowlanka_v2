from django import forms

from .models import Appointment, Comment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['description', 'date']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content']
