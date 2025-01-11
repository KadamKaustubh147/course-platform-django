from django.db import models

# Create your models here.

class Email(models.Model):
    email = models.EmailField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True) # set at creation
    
class EmailVerificationEvent(models.Model):
    parent = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True)
    '''
    models.SET_NULL:

    Sets the foreign key field in the child object to NULL when the referenced parent object is deleted.
    Requires the foreign key field to allow null=True.
    Example use: If deleting a category doesn't delete the associated products but sets their category to NULL.
    
    '''
    email = models.EmailField()
    # token
    attempts = models.IntegerField(default=0)
    expired = models.BooleanField(default=False)
    
    last_attempt_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        null=True, 
        blank=True
    )
    expired_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        null=True, 
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True) # set at creation
    
