# Generated by Django 5.1.4 on 2024-12-22 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_platform', '0009_course_created_at_lesson_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='public_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
