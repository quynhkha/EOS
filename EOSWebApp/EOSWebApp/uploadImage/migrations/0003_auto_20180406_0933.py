# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-06 09:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('uploadImage', '0002_uploadedimage_dist_per_pixel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedimage',
            name='uploaded_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 6, 9, 33, 41, 249960, tzinfo=utc)),
        ),
    ]