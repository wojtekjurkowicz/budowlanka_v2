from django import forms
from .models import Appointment, Comment


class AppointmentForm(forms.ModelForm):
    """
    Form for creating and updating Appointment instances.

    Inherits from ModelForm to automatically generate fields based on the Appointment model.

    Attributes:
        Meta (class): Metadata class for defining the model and form behavior.
            model (Appointment): Specifies the model to be used with the form.
            fields (list): List of fields from the Appointment model to include in the form.
            widgets (dict): Customizes the appearance and behavior of form fields using widgets.
    """
    class Meta:
        model = Appointment
        fields = ['description', 'date']  # Fields to be included in the form
        widgets = {
            'description': forms.Textarea(
                attrs={'placeholder': 'Opis', 'style': 'width: 300px', 'class': 'form-control'}),
            'date': forms.DateInput(attrs={'style': 'width: 300px', 'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    """
    Form for creating and updating Comment instances.

    Inherits from ModelForm to automatically generate fields based on the Comment model.

    Attributes:
        Meta (class): Metadata class for defining the model and form behavior.
            model (Comment): Specifies the model to be used with the form.
            fields (list): List of fields from the Comment model to include in the form.
            widgets (dict): Customizes the appearance and behavior of form fields using widgets.
    """
    class Meta:
        model = Comment
        fields = ['content']  # Field to be included in the form
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Treść komentarza', 'style': 'width: 100%; height: 90px',
                                             'class': 'form-control'})  # Customize the textarea widget with a CSS class
        }


class ContactForm(forms.Form):
    """
    Simple contact form for collecting user messages.

    Attributes:
        first_name (CharField): Field for the first name with customized widget attributes.
        last_name (CharField): Field for the last name with customized widget attributes.
        email (EmailField): Field for the email address with customized widget attributes.
        message (CharField): Field for the message content with a textarea widget and customized attributes.
    """
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Imie', 'style': 'width: 300px', 'class': 'form-control'}))  # Field for the first name
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Nazwisko', 'style': 'width: 300px', 'class': 'form-control'}))  # Field for the last name
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email', 'style': 'width: 300px',
                                                                     'class': 'form-control'}))  # Field for the
    # email address
    message = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': 'Wiadomość', 'style': 'width: 300px',
               'class': 'form-control'}))  # Field for the message content with a textarea widget
