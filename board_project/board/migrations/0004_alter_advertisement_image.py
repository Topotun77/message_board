# Generated by Django 5.0.3 on 2024-12-13 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_advertisement_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
