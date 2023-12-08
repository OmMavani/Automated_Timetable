from django.db import models

# Create your models here.

class Course(models.Model) : 
    name = models.CharField(max_length=20)
    labs = models.IntegerField()
    lectures = models.IntegerField()
    semester = models.IntegerField()
    classes = models.IntegerField()
    classId = models.CharField(max_length=10)