from django.db import models

class Log(models.Model):
    init_time = models.FloatField(default=0.0, verbose_name="init_time")
    final_time =  models.FloatField(default=0.0, verbose_name="final_time")
    velocity = models.FloatField(default=0.0, verbose_name="velocity")
    image = models.BinaryField(verbose_name="image")
    prompt = models.CharField(default='', verbose_name="prompt")
    trajet = models.CharField(default='', verbose_name="tarjet")
    initial_pose_X = models.FloatField(default=0.0, verbose_name="initial_pose_X")
    initial_pose_Y = models.FloatField(default=0.0, verbose_name="initial_pose_Y")
    final_pose_X = models.FloatField(default=0.0, verbose_name="final_pose_X")
    final_pose_Y = models.FloatField(default=0.0, verbose_name="final_pose_Y")
    
    
    class Meta:
        ordering = ['-init_time']