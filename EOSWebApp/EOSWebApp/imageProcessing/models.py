import os

import cv2
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.files.base import ContentFile
from django.db import models
from django.dispatch import receiver
from EOSWebApp.utils import cv_to_bytesIO, compress_image


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
            try:  # need try catch
                image_data = cv2.imread(self.image.path)
                thumbnail_cv = compress_image(image_data)

                thumbnail_full_name = self.image.name.split('/')[
                                          -1] + "_thumb" + ".jpg"  # image.name contains images/image_name
                thumbnail_bytesIO = cv_to_bytesIO(thumbnail_cv)
                self.thumbnail.save(thumbnail_full_name, content=ContentFile(thumbnail_bytesIO.getvalue()), save=False)
            except:
                pass
        super(UploadedImage, self).save(*args, **kwargs)

    def delete(self):
        # uploaded_image = UploadedImage.objects.filter(self)
        _delete_file(self.image.path)
        _delete_file(self.thumbnail.path)
        super(UploadedImage, self).delete()


class CrystalMask(models.Model):
    # TODO: add crystal image field
    image = models.ForeignKey(UploadedImage, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="no name")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    mask_dir = models.CharField(max_length=255, blank=True)

    @classmethod
    def create(cls, image, mask_dir):
        return cls(image=image, mask_dir=mask_dir)


class TempMask(models.Model):
    mask = models.ImageField(upload_to='temp_masks/', null=True)

    def save(self, mask_data=None):
        if mask_data:
            mask_full_name = self.image.name.split('/')[-1] + "_mask.png"
            mask_bytesIO = cv_to_bytesIO(mask_data, format="PNG")
            self.mask.save(mask_full_name, content=ContentFile(mask_bytesIO.getvalue()), save=False)

        super(TempMask, self).save()


class TempImage(models.Model):
    # TODO: associate with upload image
    mask = models.ForeignKey(TempMask, default=1, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='temp_images/')
    thumbnail = models.ImageField(upload_to='temp_thumbnails/', null=True)

    func_name = models.CharField(max_length=255, null=True, blank=True)
    func_setting = models.CharField(max_length=255, null=True, blank=True)
    gray_levels = ArrayField(ArrayField(models.IntegerField(null=True, blank=True)))
    k_labels = ArrayField(models.IntegerField(null=True, blank=True))

    def save(self, image_name, image_data, func_name, mask, func_setting='', gray_levels= [], k_labels = [] ):
        self.func_name = func_name
        self.func_setting = func_setting
        self.mask = mask
        self.gray_levels = gray_levels
        self.k_labels = k_labels
        image_full_name = image_name + ".jpg"
        image_bytesIO = cv_to_bytesIO(image_data)
        self.image.save(image_full_name, content=ContentFile(image_bytesIO.getvalue()), save=False)

        thumbnail_full_name = image_name + "_thumb" + ".jpg"
        thumbnail_cv = compress_image(image_data)
        thumbnail_bytesIO = cv_to_bytesIO(thumbnail_cv)
        self.thumbnail.save(thumbnail_full_name, content=ContentFile(thumbnail_bytesIO.getvalue()), save=False)
        super(TempImage, self).save()

    def delete(self):
        _delete_file(self.image.path)
        _delete_file(self.thumbnail.path)
        super(TempImage, self).delete()


def _delete_file(path):
    """ Deletes file from filesystem. """
    print(path)
    if os.path.isfile(path):
        os.remove(path)


# @receiver(models.signals.pre_delete, sender=UploadedImage)
# def delete_file(sender, instance, *args, **kwargs):
#     """ Deletes thumbnail files on `post_delete` """
#
#     if instance.image:
#         _delete_file(instance.image.path)
#     if instance.thumbnail:
#         _delete_file(instance.thumbnail.path)

#
# @receiver(models.signals.post_delete, sender=TempImage)
# def delete_file(sender, instance, *args, **kwargs):
#     """ Deletes thumbnail files on `post_delete` """
#
#     if instance.image:
#         _delete_file(instance.image.path)
#     if instance.thumbnail:
#         _delete_file(instance.thumbnail.path)
#
#
# @receiver(models.signals.post_delete, sender=TempMask)
# def delete_file(sender, instance, *args, **kwargs):
#     """ Deletes thumbnail files on `post_delete` """
#
#     if instance.mask:
#         _delete_file(instance.mask.path)
