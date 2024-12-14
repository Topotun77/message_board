# Generated by Django 5.0.3 on 2024-12-10 18:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('preference_id', models.AutoField(primary_key=True, serialize=False)),
                ('theme', models.CharField(choices=[('light', 'Light Theme'), ('dark', 'Dark Theme')], max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='preferences',
            constraint=models.UniqueConstraint(fields=('user',), name='One Entry Per User'),
        ),
    ]
