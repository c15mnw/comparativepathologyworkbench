# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-19 11:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20181119_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cell',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Image'),
        ),
    ]