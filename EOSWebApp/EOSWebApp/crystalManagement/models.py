from django.contrib.postgres.fields import ArrayField
from django.core.files.base import ContentFile
from django.db import models

# Create your models here.
from EOSWebApp.imageProcessing.models import CrystalMask
from EOSWebApp.utils import cv_to_bytesIO, _delete_file


class Crystal(models.Model):
    mask = models.ForeignKey(CrystalMask, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    crystal =  models.ImageField(upload_to="crystals/", null=True)
    pixel_area = models.IntegerField(null=True)
    real_area = models.IntegerField(null=True)
    mean = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    standard_deviation = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    height = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    # dir = models.CharField(max_length=255, blank=True)
    #
    # @classmethod
    # def create(cls, mask, name, crystal_dir):
    #     return cls(mask=mask, name=name, crystal_dir=crystal_dir)

    def save(self, mask=None, name=None, crystal_data=None, pixel_area=None, real_area=None, mean=None, \
                standard_deviation=None, height=None, width=None):
        if crystal_data is not None:
            self.mask = mask
            self.name = name
            self.pixel_area = pixel_area
            self.real_area = real_area
            self.mean = mean
            self.standard_deviation = standard_deviation
            self.height = height
            self.width = width
            self.shape = (height, width)
            crystal_bytesIO = cv_to_bytesIO(crystal_data, format="PNG")
            self.crystal.save(name + '.png', content=ContentFile(crystal_bytesIO.getvalue()), save=False)
        super(Crystal, self).save()

    def delete(self):
        _delete_file(self.crystal.path)
        super(Crystal, self).delete()

class Histogram(models.Model):
    crystal = models.ForeignKey(Crystal, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # hist_x = ArrayField(
    #         models.IntegerField(blank=True),
    #         size=256)
    # hist_y = ArrayField(
    #     models.IntegerField(blank=True),
    #     size = 256
    # )
    # similarities = ArrayField(
    #     models.FloatField(blank=True)
    # )
    hist_area = models.IntegerField(blank=True)
    num_pair = models.IntegerField(blank=True)
    overall_sim = models.IntegerField(blank=True)

    @classmethod
    def create(cls, crystal, name):
        return cls(crystal=crystal, name=name)
