from django import forms

from EOSWebApp.uploadImage.models import *

class ImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['description', 'image']
        # fields = '__all__'
