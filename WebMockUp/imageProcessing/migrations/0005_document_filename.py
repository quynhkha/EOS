# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-30 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageProcessing', '0004_numberinput'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='filename',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]