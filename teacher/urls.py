from django.urls import path
from . import views

urlpatterns=[
    path('', views.display, name='teacher'),
    path('addTeacher/', views.addTeacher, name='addTeacher'),
    path('selectCourses/', views.selectCourses, name='selectCourses'),
]