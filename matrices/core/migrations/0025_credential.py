# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-12-11 15:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0024_blog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('wordpress', models.IntegerField(default=0)),
                ('apppwd', models.CharField(default='', max_length=50)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]