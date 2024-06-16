from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User



class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'placeholder':'Email','style':'width: 300px','class': 'form-control padding'}), required=True)
    username = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Nazwa użytkownika','style':'width: 300px','class': 'form-control padding'}),required=True)
    password1 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder':'Hasło','style':'width: 300px','class': 'form-control padding'}), required=True, min_length=8)
    password2 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder':'Powtórz Hasło','style':'width: 300px','class': 'form-control padding'}), required=True, min_length=8)
    class Meta():
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserAuth(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Nazwa użytkownika','style':'width: 300px','class': 'form-control'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło', 'style': 'width: 300px', 'class': 'form-control'}))
    class Meta():
        model = User
        fields = ('username', 'password')
