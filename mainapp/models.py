import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Appointment(models.Model):
    """
    Represents a scheduled meeting or event.

    Attributes:
        description (str): The description of the appointment.
        date (datetime): The date and time of the appointment.
    """
    description = models.CharField(max_length=500, verbose_name="Opis projektu")  # Description of the appointment
    date = models.DateTimeField(default=timezone.now, verbose_name="Data")  # Date and time of the appointment

    def __str__(self):
        """
        Returns a string representation of the appointment.

        Returns:
            str: The description of the appointment.
        """
        return self.description

    class Meta:
        verbose_name_plural = "Wizyty"  # Plural name for the Appointment model


class Realization(models.Model):
    """
    Represents a project or task completion.

    Attributes:
        title (str): The title of the realization.
        content (str): The description of the realization.
        date (datetime): The date and time when the realization was added.
    """
    title = models.CharField(max_length=100, verbose_name="Tytuł")  # Title of the realization
    content = models.CharField(max_length=500, verbose_name="Opis")  # Description of the realization
    date = models.DateTimeField(default=timezone.now,
                                verbose_name="Data dodania")  # Date and time when the realization was added

    # Path to file (currently commented out)
    # image = models.CharField(max_length=50)

    def was_published_recently(self):
        """
        Checks if the realization was published within the last day.

        Returns:
            bool: True if the realization was published within the last day, False otherwise.
        """
        return self.date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        """
        Returns a string representation of the realization.

        Returns:
            str: The first 25 characters of the content.
        """
        return f"{self.content[:25]}..."  # Return the first 25 characters of the content

    class Meta:
        verbose_name_plural = "Realizacje"  # Plural name for the Realization model
        ordering = ['date']  # Default ordering by date


class Comment(models.Model):
    """
    Represents feedback or notes on a realization.

    Attributes:
        realization (Realization): The associated realization.
        author (User): The author of the comment.
        content (str): The content of the comment.
        date (datetime): The date and time when the comment was added.
    """
    realization = models.ForeignKey(Realization, on_delete=models.CASCADE,
                                    verbose_name="Realizacja")  # Associated realization
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor komentarza')  # Author of the comment
    content = models.CharField(max_length=200, verbose_name='')  # Content of the comment
    date = models.DateTimeField(default=timezone.now, verbose_name='Data')  # Date and time when the comment was added

    def __str__(self):
        """
        Returns a string representation of the comment.

        Returns:
            str: The content of the comment.
        """
        return self.content

    class Meta:
        verbose_name_plural = "Komentarze"  # Plural name for the Comment model
