from django.contrib.auth.models import User
from django.forms import forms, ModelForm


class UserForm(ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput) # for showing the password as hidden text

    class Meta:
        model = User
        fields = ['username', 'email', 'password']