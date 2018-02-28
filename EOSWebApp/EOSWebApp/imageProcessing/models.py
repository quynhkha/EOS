from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# class Image (models.Model):
#     imageName = models.CharField(max_length=250)
#     imageType = models.CharField(max_length=10)
#     imageLink = models.CharField(max_length=1000)
#     imageData = models.FileField(null= True)
#
#     def __str__(self):
#         return self.imageName + '.' +self.imageType

class UploadedImage(models.Model):
    user = models.ForeignKey(User, default=1)
    description = models.CharField(max_length=255, blank=True)
    document = models.ImageField(upload_to="images/")
    filename = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    thumbnail_url = models.CharField(max_length=255, blank=True)
    # thumbnail = models.ImageField(upload_to="documents/", blank=True)
    #
    # def __str__(self):
    #    return self.document

class CrystalMask(models.Model):
    # TODO: add crystal image field
    image = models.ForeignKey(UploadedImage, default=1)
    name = models.CharField(max_length=255, default="no name")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    mask_dir = models.CharField(max_length=255, blank=True)

    @classmethod
    def create(cls, image, mask_dir):
        return cls(image=image, mask_dir=mask_dir)

