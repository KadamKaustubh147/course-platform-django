from django.db import models

# Create your models here.

class status(models.TextChoices):
    Published = "Published"
    Draft = "Draft"
    Coming = "Coming_Soon"

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # image = models.ImageField(upload_to='images')
    
    access = [
        ("Anyone", "Anyone"),
        ("Email", "Email_Required"),
        # "Purchase": "Purchase_Required",
        # "User": "User_Required",
    ],
    
    status = models.CharField(
        max_length=255,
        choices=status.choices,
        default=status.Draft
    )

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=255,
        choices=status.choices,
        default=status.Draft
    )