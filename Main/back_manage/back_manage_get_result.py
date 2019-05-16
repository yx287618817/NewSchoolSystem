# -*- coding: utf-8 -*-
# @Time    : 2019-05-12 15:55
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : back_manage_get_result.py
# @Software: PyCharm


# 生成教师学号
import datetime
import random
from .. import models
from . import back_manage_forms as myforms
from django.shortcuts import render, HttpResponse, HttpResponseRedirect


def many_many_select(req, n1, n2, m, m1, m2, form, upt=True):
    name_one = n1
    name_two = n2
    if req.method == 'GET':
        if req.GET.get('query', None) == 'delete':
            tid = req.GET.get('tid', None)
            m.objects.filter(id=tid).delete()

    if req.method == 'POST':
        if req.POST.get('res', None) == '确定增加':
            table = form(req.POST, req.FILES)
            if table.is_valid():
                data = table.cleaned_data
                try:
                    m.objects.create(**data)
                except:
                    return HttpResponse('<script>alert("重复的输入");location.href=""</script>')

    table = form()
    obj = m.objects.all()
    return render(req, 'one_select.html', locals())


def one_many_select(req, n1, n2, model, form, upt=True):
    name_one = n1
    name_two = n2
    if req.method == 'GET':
        if req.GET.get('query', None) == 'delete':
            tid = req.GET.get('tid', None)
            model.objects.filter(id=tid).delete()

    if req.method == 'POST':
        if req.POST.get('res', None) == '确定增加':
            table = form(req.POST, req.FILES)
            if table.is_valid():
                data = table.cleaned_data
                model.objects.create(**data)

    table = form()
    obj = model.objects.all()
    return render(req, 'one_select.html', locals())


def one_select(req,n1, n2, model, form, upt=True):
    name_one = n1
    name_two = n2
    if req.method == 'GET':
        if req.GET.get('query', None) == 'delete':
            tid = req.GET.get('tid', None)
            model.objects.filter(id=tid).delete()

        if req.GET.get('query', None) == 'query':
            if upt:
                tid = req.GET.get('tid', None)
                obj = model.objects.filter(id=tid).values().first()
                obj_lst =[[k, v] for k, v in obj.items()]

    if req.method == 'POST':
        if req.POST.get('res', None) == '确定增加':
            table = form(req.POST, req.FILES)
            if table.is_valid():
                data = table.cleaned_data
                model.objects.create(**data)

        else:
            if upt:
                tid = req.POST.get('id', None)
                obj = model.objects.filter(id=tid).values().first()
                data = {}
                for k in obj:
                    if k != 'id':
                        data[k] = req.POST.get(k, None)
                model.objects.filter(id=tid).update(**data)

    table = form()
    obj = model.objects.all()
    return render(req, 'one_select.html', locals())
