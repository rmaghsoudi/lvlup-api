# Generated by Django 3.0.5 on 2020-05-18 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_user_xp_to_lvlup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='xp_to_lvlup',
        ),
    ]
