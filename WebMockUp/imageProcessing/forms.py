from django import forms
from .models import Post, Document

class NameForm(forms.Form):
    your_name = forms.CharField (label = 'Your name', max_length = 100)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', )

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        # field = ('desciption', 'document', )
        fields = '__all__'