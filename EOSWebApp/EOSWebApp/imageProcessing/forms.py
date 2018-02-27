from django import forms

from .models import *

class ImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['description', 'document']
        # fields = '__all__'
