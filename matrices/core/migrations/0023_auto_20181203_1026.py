# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-12-03 10:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20181127_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='pwd',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='server',
            name='uid',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]