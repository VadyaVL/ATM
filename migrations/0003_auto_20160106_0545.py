# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-06 03:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ATM', '0002_auto_20160106_0534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankcard',
            name='Locked',
            field=models.BooleanField(default=False, verbose_name=b'\xd0\x97\xd0\xb0\xd0\xb1\xd0\xbb\xd0\xbe\xd0\xba\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb0\xd1\x8f'),
        ),
        migrations.AlterField(
            model_name='bankcard',
            name='Number',
            field=models.TextField(primary_key=True, serialize=False, verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80'),
        ),
        migrations.AlterField(
            model_name='bankcard',
            name='Password',
            field=models.TextField(verbose_name=b'\xd0\x9f\xd0\xb0\xd1\x80\xd0\xbe\xd0\xbb\xd1\x8c'),
        ),
    ]
