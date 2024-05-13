from django.db import models


class Appointment(models.Model):
    # An appointment class
    description = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

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
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    # Path to file
    # image = models.CharField(max_length=50)

    def __str__(self):
        """Return a string representation"""
        return f"{self.content[:10]}..."


class Comments(models.Model):
    """A comments class"""
    realization = models.ForeignKey(Realization, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation"""
        return self.content


"""
class User(models.Model):
    # A user class
    nick = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=40)
    e_mail = models.CharField(max_length=40)
    password = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        # Return a string representation
        return self.nick
"""