# Generated by Django 5.1.4 on 2024-12-18 20:37

import board.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0010_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=board.models.user_directory_path),
        ),
    ]