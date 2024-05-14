import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Appointment(models.Model):
    # An appointment class
    description = models.CharField(max_length=500, verbose_name="Opis projektu")
    date = models.DateTimeField(default=timezone.now, verbose_name="Data")

    def __str__(self):
        # Return a string representation
        return self.description


class Message(models.Model):
    # A message class
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    content = models.CharField(max_length=160)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Return a string representation
        return self.content


class Realization(models.Model):
    """A realization class"""
    title = models.CharField(max_length=100, verbose_name="Tytuł")
    content = models.CharField(max_length=500, verbose_name="Opis")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Data dodania")

    # Path to file
    # image = models.CharField(max_length=50)

    def was_published_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        """Return a string representation"""
        return f"{self.content[:10]}..."


class Comment(models.Model):
    """A comments class"""
    realization = models.ForeignKey(Realization, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation"""
        return self.content
