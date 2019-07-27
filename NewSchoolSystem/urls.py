"""学校管理项目 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from NewSchoolSystem.settings import STATIC_ROOT
from templates.SQL即查即用 import MySqlControl



urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^back_manage/', include('Main.back_manage.back_manage_urls')),
    url(r'^teacher_manage/', include('Main.teacher.urls')),
    url(r'', include('Main.urls')),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


