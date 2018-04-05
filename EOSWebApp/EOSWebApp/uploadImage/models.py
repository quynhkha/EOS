import cv2
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models

# Create your models here.
from EOSWebApp.utils import compress_image, cv_to_bytesIO, _delete_file


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
