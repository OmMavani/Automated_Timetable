from django.shortcuts import render, redirect
from .models import *
from course.models import *
# Create your views here.

def addTeacher(request) : 
    if request.method == 'POST' : 
        name = request.POST['name']
        priority = request.POST['priority']
        teacherid = request.POST['teacherId']
        obj = Teacher(name=name, priority=priority, teacherid=teacherid)
        obj.save()
    return render(request, "addTeacher.html")

def selectCourses(request) : 
    options = 10
    choices = Course.objects.all()
    teachers = Teacher.objects.all()
    if request.method == 'POST' : 
        name = request.POST['name']
        selection = {}
        for i in range(0, options) : 
            nameStr = "id" + str(i);
            selection[nameStr] = request.POST[nameStr]
        obj = Selection(name=name, options=selection)
        obj.save()
    context = {'teachers' : teachers, 'courses' : choices, 'options': range(options)}
    return render(request, "selection.html", context)

def display(request) : 
    return render(request, 'displayForTeacher.html')