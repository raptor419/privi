# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from app import views

urlpatterns = [

]

urlpatterns = [
    # Matches any html file 
    re_path(r'^.*\.html', views.pages, name='pages'),
    path('', views.index, name='home'),
    path('api_get_quiz', views.make_quiz),
]
