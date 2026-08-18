from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    pass

class Log(models.Model):
    date = models.DateTimeField()
    ip = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='logs')

class Mission(models.Model):
    class State(models.TextChoices):
        ACCEPTED = 'ACC', 'Accepted'
        REJECTED = 'REJ', 'Rejected'
    state = models.CharField(max_length=3, choices=State.choices, default=State.ACCEPTED)
    distance = models.IntegerField()
    time = models.TimeField()
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    log = models.OneToOneField(Log, on_delete=models.CASCADE, related_name='mission')

class Prompt(models.Model):
    prompt = models.CharField(max_length=255)
    object = models.CharField(max_length=255)
    bbox = models.ImageField(upload_to='bboxes/')
    mission = models.OneToOneField(Mission, on_delete=models.CASCADE, related_name='prompt')

class Goal(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    mission = models.OneToOneField(Mission, on_delete=models.CASCADE, related_name='goal')

    