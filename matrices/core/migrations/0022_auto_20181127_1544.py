# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-27 15:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20181127_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='core.Type'),
        ),
    ]