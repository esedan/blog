# Generated by Django 5.0.1 on 2024-02-08 20:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=50)),
                ('Content', models.TextField(max_length=1000)),
                ('Date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
