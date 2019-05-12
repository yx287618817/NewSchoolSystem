# -*- coding: utf-8 -*-
# @Time    : 2019-04-25 18:11
# @Author  : Paul
# @Email   : 287618817@qq.com
# @File    : myforms.py
# @Software: PyCharm
from django import forms
from django.forms import widgets
from .. import models

USER = models.User.objects.all()
GROUP = models.Group.objects.all()


class Group(forms.Form):
    groupName = forms.CharField(label='用户组名字', widget=widgets.Input(attrs={
        'placeholder': '请输入新建用户组',
    }))

class UserGroup(forms.Form):

    user = forms.ModelChoiceField(label='用户', queryset=USER)
    group = forms.ModelChoiceField(label='用户组', queryset=GROUP)

class User(forms.Form):
    pass

