from django.urls import path
from . import views

urlpatterns=[
    path('addCourse/', views.addCourse, name='addCourse'),
]