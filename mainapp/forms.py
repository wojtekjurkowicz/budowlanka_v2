from django import forms


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
