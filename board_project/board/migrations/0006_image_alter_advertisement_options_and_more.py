# Generated by Django 5.1.4 on 2024-12-14 22:55

import board.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_alter_advertisement_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank=True, null=True, upload_to=board.models.user_directory_path, verbose_name='Файл')),
            ],
        ),
        migrations.AlterModelOptions(
            name='advertisement',
            options={'verbose_name': 'Объявление', 'verbose_name_plural': 'Объявление'},
        ),
        migrations.RemoveConstraint(
            model_name='preferences',
            name='One Entry Per User',
        ),
        migrations.AddConstraint(
            model_name='preferences',
            constraint=models.UniqueConstraint(fields=('user',), name='Одна запись на пользователя'),
        ),
        migrations.AddField(
            model_name='image',
            name='advertisement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='board.advertisement'),
        ),
        migrations.AddField(
            model_name='image',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
