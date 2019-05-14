# -*- coding: utf-8 -*-
# @Time    : 2019-04-25 16:58
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from . import back_manage_views as views

urlpatterns = [
    url(r'^user_manage/$', views.user_manage, name='user_manage.html'),
    url(r'^group_manage/$', views.group_manage, name='group_manage.html'),
    url(r'^group_permission/$', views.group_permission, name='group_permission.html'),
    url(r'^table_manage/$', views.table_manage, name='one_select.html'),
    url(r'^table_permission/$', views.table_permission, name='one_select.html'),
    url(r'^sex_manage/$', views.sex_manage, name='one_select.html'),
    url(r'^student_status/$', views.student_status, name='one_select.html'),
    url(r'^student_type/$', views.student_type, name='one_select.html'),
    url(r'^major_manage/$', views.major_manage, name='one_select.html'),
    url(r'^$', views.back_manage_index, name='back_manage_index.html'),
]
