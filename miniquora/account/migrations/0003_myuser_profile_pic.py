# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-06 01:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20170104_0206'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
