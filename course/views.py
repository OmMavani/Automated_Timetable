from django.shortcuts import render
from .models import *
# Create your views here.

def addCourse(request) : 
    if request.method == 'POST' : 
        name = request.POST['name']
        labs = request.POST['labs']
        lectures = request.POST['lectures']
        semester = request.POST['semester']
        classes = request.POST['classes']
        classId = request.POST['classId']
        obj = Course(name=name, labs=labs, lectures=lectures, semester=semester, classes=classes, classId=classId)
        obj.save()
    return render(request, "addCourse.html")