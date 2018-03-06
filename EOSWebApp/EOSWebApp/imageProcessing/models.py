import os

import cv2
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
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
from django.dispatch import receiver

from EOSWebApp.imageProcessing.utils import compress_image
from EOSWebApp.utils import cv_to_bytesIO


class UploadedImage(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True)
    description = models.CharField(max_length=255, blank=True)
    filename = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # thumbnail_url = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if self.image:
            try: # need try catch
                image_data = cv2.imread(self.image.path)
                thumbnail_cv = compress_image(image_data)

                thumbnail_full_name = self.image.name.split('/')[-1]+ "_thumb" + ".jpg" #image.name contains images/image_name
                thumbnail_bytesIO = cv_to_bytesIO(thumbnail_cv)
                self.thumbnail.save(thumbnail_full_name, content=ContentFile(thumbnail_bytesIO.getvalue()), save=False)
            except:
                pass
        super(UploadedImage, self).save(*args, **kwargs)



class CrystalMask(models.Model):
    # TODO: add crystal image field
    image = models.ForeignKey(UploadedImage, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="no name")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    mask_dir = models.CharField(max_length=255, blank=True)

    @classmethod
    def create(cls, image, mask_dir):
        return cls(image=image, mask_dir=mask_dir)

class TempImage(models.Model):
    image = models.ImageField(upload_to='temp_images/')
    thumbnail = models.ImageField(upload_to='temp_thumbnails/', null=True)
    def save(self, image_name, img_data):
        image_full_name = image_name+".jpg"
        image_bytesIO = cv_to_bytesIO(img_data)
        self.image.save(image_full_name, content=ContentFile(image_bytesIO.getvalue()),save = False)

        thumbnail_full_name = image_name+"_thumb"+".jpg"
        thumbnail_cv =  compress_image(img_data)
        thumbnail_bytesIO = cv_to_bytesIO(thumbnail_cv)
        self.thumbnail.save(thumbnail_full_name, content=ContentFile(thumbnail_bytesIO.getvalue()), save=False)
        super(TempImage, self).save()



    # def delete(self):
    #     tempImage = TempImage.objects.filter(=self)
    #     print
    #     self._delete_file(tempImage.image.path)
    #     self._delete_file(tempImage.thumbnail.path)
    #     super(TempImage, self).delete()

def _delete_file(path):
    """ Deletes file from filesystem. """
    print(path)
    if os.path.isfile(path):
        os.remove(path)

@receiver(models.signals.pre_delete, sender=TempImage)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes thumbnail files on `post_delete` """

    if instance.image:
        _delete_file(instance.image.path)
    if instance.thumbnail:
        _delete_file(instance.thumbnail.path)

@receiver(models.signals.pre_delete, sender=UploadedImage)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes thumbnail files on `post_delete` """

    if instance.image:
        _delete_file(instance.image.path)
    if instance.thumbnail:
        _delete_file(instance.thumbnail.path)

