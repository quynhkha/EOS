from django.db import models

# Create your models here.

class Image (models.Model):
    imageName = models.CharField(max_length=250)
    imageType = models.CharField(max_length=10)
    imageLink = models.CharField(max_length=1000)
    imageData = models.FileField(null= True)

    def __str__(self):
        return self.imageName + '.' +self.imageType

class Post (models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=100)

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
