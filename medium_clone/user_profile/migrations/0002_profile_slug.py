# Generated by Django 5.0.2 on 2024-03-05 16:02

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True),
        ),
    ]
