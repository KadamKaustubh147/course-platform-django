# Generated by Django 5.1.4 on 2025-01-18 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
