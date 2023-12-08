from django.db import models

# Create your models here.

class Teacher(models.Model) : 
    name = models.CharField(max_length=20)
    priority = models.FloatField()
    teacherid = models.CharField(max_length=10)


class Selection(models.Model):
    name = models.CharField(max_length=20)
    options = models.JSONField()