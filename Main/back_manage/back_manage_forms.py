# -*- coding: utf-8 -*-
# @Time    : 2019-04-25 18:11
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : myforms.py
# @Software: PyCharm
from django import forms
from django.forms import widgets
from .. import models

USER = models.RegisterFirst.objects.all()
GROUP = models.Group.objects.all()


class Group(forms.Form):
    groupName = forms.CharField(label='用户组名字', widget=widgets.Input(attrs={
        'placeholder': '请输入新建用户组',
    }))

class UserGroup(forms.Form):
    user = forms.ModelChoiceField(label='用户', queryset=USER)
    group = forms.ModelChoiceField(label='用户组', queryset=GROUP)


class Table(forms.Form):
    caption = forms.CharField(label='操作表名')
    tableName = forms.CharField(label='操作路径', widget=widgets.Input(attrs={
        'onchange': 'check_file()',
    }))


class TablePermission(forms.Form):
    caption = forms.CharField(label='权限名称')
    tableUrl = forms.CharField(label='权限路径')


class Major(forms.Form):
    image = forms.ImageField(label='总专业照片')
    caption = forms.CharField(label='专业名字')


class Sex(forms.Form):
    sex = forms.CharField(label='性别')


class StudentStatus(forms.Form):
    student_status = forms.CharField(label='学生状态')


class StudentType(forms.Form):
    student_type = forms.CharField(label='生源类型')
