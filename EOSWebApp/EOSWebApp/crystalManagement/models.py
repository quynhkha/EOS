from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
from EOSWebApp.imageProcessing.models import CrystalMask


class Crystal(models.Model):
    mask = models.ForeignKey(CrystalMask, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dir = models.CharField(max_length=255, blank=True)

    @classmethod
    def create(cls, mask, name, crystal_dir):
        return cls(mask=mask, name=name, crystal_dir=crystal_dir)

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
