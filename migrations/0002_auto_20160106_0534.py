# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-06 03:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ATM', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankcard',
            name='Balance',
            field=models.FloatField(verbose_name=b'\xd0\x91\xd0\xb0\xd0\xbb\xd0\xb0\xd0\xbd\xd1\x81'),
        ),
    ]
