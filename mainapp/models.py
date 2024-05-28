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

    class Meta:
        verbose_name_plural = "Wizyty"


class Message(models.Model):
    # A message class
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    content = models.CharField(max_length=160, verbose_name="Treść")
    date = models.DateTimeField(default=timezone.now, verbose_name="Data")

    def __str__(self):
        # Return a string representation
        return self.content

    class Meta:
        verbose_name_plural = "Wiadomości"


class Realization(models.Model):
    """A realization class"""
    title = models.CharField(max_length=100, verbose_name="Tytuł")
    content = models.CharField(max_length=500, verbose_name="Opis")
    date = models.DateTimeField(default=timezone.now(), verbose_name="Data dodania")

    # Path to file
    # image = models.CharField(max_length=50)

    def was_published_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        """Return a string representation"""
        return f"{self.content[:25]}..."

    class Meta:
        verbose_name_plural = "Realizacje"


class Comment(models.Model):
    """A comments class"""
    realization = models.ForeignKey(Realization, on_delete=models.CASCADE, verbose_name="Realizacja")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor komentarza')
    content = models.CharField(max_length=200, verbose_name='Treść komentarza')
    date = models.DateTimeField(default=timezone.now, verbose_name='Data')

    def __str__(self):
        """Return a string representation"""
        return self.content

    class Meta:
        verbose_name_plural = "Komentarze"
