# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-27 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageProcessing', '0003_document_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='NumberInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input', models.IntegerField()),
            ],
        ),
    ]
