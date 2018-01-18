# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-10 09:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageProcessing', '0011_auto_20180109_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='crystalmask',
            name='name',
            field=models.CharField(default='no name', max_length=255),
        ),
        migrations.AlterField(
            model_name='uploadedimage',
            name='document',
            field=models.ImageField(upload_to='images/'),
        ),
    ]