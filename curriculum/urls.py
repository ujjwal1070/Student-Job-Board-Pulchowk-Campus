from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from .views import *


app_name = "curriculum"

urlpatterns = [
    
    path('classic/',export_classic,name='classic'),
    path('classic1/',export_classic1,name='classic1'),
    path('modern/',export_single_page,name='modern'),
    #path('htmltest/<str:first_name>/',export_class,name='test'),
    path('htmltest/',export_class,name='test'),
    path('language/',addlanguage,name='language'),
    path('languageitem/',addlanguageitem,name='languageitem'),
    path('resume/',addresume,name='resume'),
    path('skill/',addskill,name='skill'),
    path('skillitem/',addskillitem,name='skillitem'),
    path('certification/',addcertification,name='certification'),
    path('certificationitem/',addcertificationitem,name='certificationitem'),
    path('experience/',addexperience,name='experience'),
    path('project/',addproject,name='project'),
    path('projectitem/',addprojectitem,name='projectitem'),
    path('training/',addtraining,name='training'),
    path('edit_profile',menulist,name='showmenu'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)