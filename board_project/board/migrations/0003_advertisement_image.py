# Generated by Django 5.0.3 on 2024-12-13 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_preferences_preferences_one_entry_per_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='image',
            field=models.ImageField(null=True, upload_to='image/'),
        ),
    ]