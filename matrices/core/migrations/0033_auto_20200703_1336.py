# Generated by Django 3.0.3 on 2020-07-03 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_authorisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorisation',
            name='matrix',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Matrix'),
        ),
    ]
