# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path

def home(request):
    from django.http import HttpResponse
    return HttpResponse("Django is working!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home)
]