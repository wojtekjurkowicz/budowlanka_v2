import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Realization(models.Model):
    """
    Represents a project or task completion.

    Attributes:
        title (str): The title of the realization.
        content (str): The description of the realization.
        date (datetime): The date and time when the realization was added.
    """
    title = models.CharField(max_length=100, verbose_name="Tytuł")  # Title of the realization
    content = models.CharField(max_length=1000, verbose_name="Opis")  # Description of the realization
    date = models.DateTimeField(default=timezone.now,
                                verbose_name="Data dodania")  # Date and time when the realization was added
    image = models.ImageField(upload_to='realizations_images/', null=True, blank=True, verbose_name="Zdjęcie główne") # Image of the realization

    def __str__(self):
        """
        Returns a string representation of the realization.

        Returns:
            str: Title of the realization.
        """
        return self.title

    class Meta:
        verbose_name_plural = "Realizacje"  # Plural name for the Realization model
        ordering = ['-date']  # Default ordering by date


class RealizationImage(models.Model):
    """
    Represents a project image.

    Attributes:
        realization (Realization): The associated realization.
        image (str): Image of the realization.
    """
    realization = models.ForeignKey(Realization, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='realizations_images/')

    def __str__(self):
        return f"{self.realization.title} Image"
