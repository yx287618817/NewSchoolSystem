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


def one_select(req, model, form):
    if req.method == 'GET':
        if req.GET.get('query', None) == 'delete':
            tid = req.GET.get('tid', None)
            model.objects.filter(id=tid).delete()

        if req.GET.get('query', None) == 'query':
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
