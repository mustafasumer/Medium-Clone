# Generated by Django 5.0.2 on 2024-03-06 14:23

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Post',
            new_name='BlogPost',
        ),
    ]
