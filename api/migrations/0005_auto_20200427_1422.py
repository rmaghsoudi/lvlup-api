# Generated by Django 3.0.5 on 2020-04-27 14:22

import api.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200425_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='entry',
            name='type',
            field=models.CharField(blank=True, max_length=6, validators=[api.validators.validate_type]),
        ),
    ]