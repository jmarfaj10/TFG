from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator

class User(AbstractUser):
    username_validator = RegexValidator(
          regex=r'^[a-z0-9_]{3,20}$',
          message='Only lowercase letters, numbers and underscore, between 3 and 20 characters.'
    )
    
    username = models.CharField(
          'username',
          max_length=20,
          unique=True,
          help_text='Only lowercase letters, numbers and underscore, between 3 and 20 characters.',
          validators=[username_validator],
          error_messages={'unique': 'A user with that username already exists.'},
    )   

class Log(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=45)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='logs')

class Mission(models.Model):
    class State(models.TextChoices):
        REACHED = 'REACHED', 'Reached'
        NOT_REACHED = 'NOT_REACHED', 'Not Reached'
        REJECTED = 'REJECTED', 'Rejected'
        
    state = models.CharField(max_length=11, choices=State.choices, default=State.REACHED)
    distance = models.FloatField(null=True)
    time = models.DurationField(null=True)
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    z = models.FloatField(null=True)
    log = models.OneToOneField(Log, on_delete=models.CASCADE, related_name='mission')

class Prompt(models.Model):
    prompt = models.CharField()
    object = models.CharField(max_length=255)
    bbox = models.ImageField(upload_to='bboxes/', blank=True, null=True)
    mission = models.OneToOneField(Mission, on_delete=models.CASCADE, related_name='prompt')

class Goal(models.Model):
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    z = models.FloatField(null=True)
    mission = models.OneToOneField(Mission, on_delete=models.CASCADE, related_name='goal')

    