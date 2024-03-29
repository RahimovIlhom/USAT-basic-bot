# Generated by Django 4.2.11 on 2024-03-28 23:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lid_app', '0002_postimage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postimage',
            options={'ordering': ['-created_time']},
        ),
        migrations.AddField(
            model_name='postimage',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
