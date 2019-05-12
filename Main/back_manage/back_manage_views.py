# -*- coding: utf-8 -*-
# @Time    : 2019-04-25 16:58
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : views.py
# @Software: PyCharm
import json

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from . import back_manage_forms as myforms
from .. import models


# 用户分配用户组
def user_group_manage(request):
    user_group = myforms.UserGroup()
    return render(request, 'user_group_manage.html', locals())


# 用户组管理
def group_manage(request):
    if request.method == 'GET':
        name = request.GET.get('name', None)
        if name == 'delete':
            gid = request.GET.get('gid', None)
            if gid:
                models.Group.objects.filter(id=gid).delete()
        if name == 'update':
            gid = request.GET.get('gid', None)
            if gid:
                group_list = []
                group = []
                group_update = models.Group.objects.filter(id=gid).first()
                return render(request, 'group_manage.html', locals())
        group = myforms.Group()
        group_list = models.Group.objects.all()
        return render(request, 'group_manage.html', locals())
    else:
        group_date = []
        if request.POST.get('add', None):
            group = myforms.Group(request.POST)
            if group.is_valid():
                data = group.cleaned_data
                models.Group.objects.create(**data)
            else:
                return render(request, 'group_manage.html', locals())

        gid = request.POST.get('gid')
        if gid:
            if request.POST.get('update', None):
                groupName = request.POST.get('groupName', None)
                models.Group.objects.filter(id=gid).update(groupName=groupName)
            else:
                return render(request, 'group_manage.html', locals())
        return HttpResponseRedirect('/back_manage/group_manage/')


def user_manage(request):
    if request.method == 'GET':
        if request.GET.get('query') == 'user':
            username = request.GET.get('user')
            user_mes = list(models.RegisterFirst.objects.filter(username=username).values_list('username', 'tel', 'number').first())
            if user_mes:
                return render(request, 'user_manage.html', locals())
            return HttpResponse('<script>alert("没有这个用户");'
                                'location.href="/back_manage/user_manage/"</script>')
        else:
            return render(request, 'user_manage.html')

    return HttpResponse(json.dumps({'res': 'ok'}))


def back_manage_index(request):
    if request.method == 'GET':
        return render(request, 'back_manage_index.html')
