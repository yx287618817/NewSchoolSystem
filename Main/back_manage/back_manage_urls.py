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
    url(r'^user_group_manange/$', views.user_group_manange, name='user_group_manange.html'),
    url(r'^$', views.back_manage_index, name='back_manage_index.html'),
]
