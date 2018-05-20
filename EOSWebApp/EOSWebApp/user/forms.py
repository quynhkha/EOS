from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput) # for showing the password as hidden text

    class Meta:
        model = User
        fields = ['username', 'password', 'email']