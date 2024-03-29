# Generated by Django 4.2.11 on 2024-03-28 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('school', models.CharField(max_length=15)),
                ('class_num', models.CharField(blank=True, max_length=15, null=True)),
                ('pinfl', models.CharField(blank=True, max_length=50, null=True)),
                ('created_time', models.DateField(auto_now_add=True)),
                ('update_time', models.DateField(auto_now=True)),
                ('invitation', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'lids',
            },
        ),
    ]