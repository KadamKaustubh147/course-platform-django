# Generated by Django 5.1.4 on 2025-01-01 08:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_platform', '0011_lesson_public_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='public_id',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson', to='course_platform.course'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='public_id',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
    ]
