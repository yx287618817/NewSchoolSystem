# -*- coding: utf-8 -*-
# @Time    : 2019-04-25 16:58
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : views.py
# @Software: PyCharm


import json
from django.db import transaction
from .back_manage_get_result import *
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from . import back_manage_forms as myforms
from .. import models


def dep_to_tea(request):
    return many_many_select(request, '教师分配系部', '已分配', models.DepToTea ,models.Major, models.RegisterFirst, myforms.DepToTea)


def work_type(request):
    return one_select(request, '工作类型管理' , '已设置工作类型', models.Work_type, myforms.Work_type)


def work_state(request):
    return one_select(request, '工作状态管理' , '已设置工作状态', models.Work_state, myforms.Work_state)

# 生成权限
def permission(request):
    return many_many_select(request, '权限管理' , '已设置权限', models.Permission, models.TableName , models.TablePermission, myforms.Permission)


# 子专业管理
def major_child(request):
    return one_many_select(request, '子专业管理' , '已设置子专业', models.MajorChild, myforms.MajorChild)


# 生源类型管理
def student_type(request):
    return one_select(request, '生源类型管理' , '已设置生源类型', models.StudentType, myforms.StudentType)


# 学生状态管理
def student_status(request):
    return one_select(request, '学生状态管理' , '已设置学生状态', models.StudentStatus, myforms.StudentStatus)


# 性别管理
def sex_manage(request):
    return one_select(request, '性别管理' , '已设置性别', models.Sex, myforms.Sex)


# 总专业管理.增加图片
def major_manage(request):
    return one_select(request, '总专业管理' , '已设置总专业', models.Major, myforms.Major, upt=False)


# 操作表权限管理
def table_permission(request,):
    return one_select(request, '子权限管理' , '已设置子权限', models.TablePermission, myforms.TablePermission)


# 操作表管理
def table_manage(request):
    return one_select(request, '主权限管理' , '已设置主权限', models.TableName, myforms.Table)


# 用户组分配权限
def group_permission(request):
    if request.method == 'GET':
        groups = models.Group.objects.all()
        if request.GET.get('query', None):
            if request.GET.get('query', None) == 'group':
                gid = request.GET.get('gid', None)
                request.session['gid'] = gid
            elif request.GET.get('query', None) == 'group_delete_permission':
                pid = request.GET.get('pid', None)
                models.GroupPermission.objects.filter(id=pid).delete()
            elif request.GET.get('query', None) == 'group_add_permission':
                pid = request.GET.get('pid', None)
                gid = request.session.get('gid')
                try:
                    models.GroupPermission.objects.create(group_id=gid, permission_id=pid)
                except Exception:
                    return HttpResponse('<script>alert("请不要快速操作");'
                                'location.href="/back_manage/group_permission/"</script>')
            gid = request.session.get('gid')
            g_obj = models.Group.objects.filter(id=gid).first()
            # 用户组已有权限
            groups__have_permission = models.GroupPermission.objects.filter(group_id=gid)
            # 用户组没有的权限
            groups__no_permission = models.Permission.objects.all().exclude(grouppermission__group_id=gid)
            return render(request, 'group_permission.html', locals())
        else:
            return render(request, 'group_permission.html', locals())


# 用户管理用户分配用户组
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
        if request.GET.get('user', None):
            request.session['user_g'] = request.GET.get('user', None)

        username = request.session.get('user_g', None)
        if request.GET.get('query') == 'usergroup_delete':
            ug_id = request.GET.get('ug_id', None)
            models.UserGroup.objects.filter(id=ug_id).delete()

        if request.GET.get('query') == 'add_user':
            sid = request.GET.get('s_id', None)
            user_obj = models.RegisterFirst.objects.filter(username=username).first()
            try:
                models.UserGroup.objects.create(user_id=user_obj.id, group_id=sid)
            except:
                return HttpResponse('<script>alert("请不要重复操作");'
                                        'location.href="/back_manage/user_manage/"</script>')

        if request.GET.get('query') == 'delete':
            models.RegisterFirst.objects.filter(username=username).delete()

        users = list(models.RegisterFirst.objects.all().exclude(
            usergroup__group__groupName__in=['学生', '管理员']).values_list('username'))

        # users = list(models.RegisterFirst.objects.all().exclude(
        # usergroup__group__groupName__in=['管理员']).values_list('username'))

        users_lst = [i for j in users for i in j]
        user_obj = models.RegisterFirst.objects.filter(username=username).first()
        if user_obj:
            user_mes = [user_obj.username, user_obj.tel, user_obj.number]
        g_lst = models.UserGroup.objects.filter(user__username=username)
        groups = models.Group.objects.exclude(usergroup__user__username=username)
        return render(request, 'user_manage.html', locals())




def back_manage_index(request):
    if request.method == 'GET':
        return render(request, 'back_manage_index.html')
