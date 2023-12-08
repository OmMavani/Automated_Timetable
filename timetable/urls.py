from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.display, name='timetable'),
    path('teacher/', views.displayTeacher, name='displayTeacher'),
    path('semester/', views.displaySemester, name='displaySemester'),
    path('generate/', views.generate, name='generate')
]