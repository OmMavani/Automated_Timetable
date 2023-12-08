from django.db import models

# Create your models here.

class Timetable(models.Model) : 
    slot = models.IntegerField()
    info = models.CharField(max_length=10)
    semester = models.IntegerField()
    div = models.CharField(max_length=1)
    teacherid = models.CharField(max_length=5)