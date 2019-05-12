import re
from . import models
from django import forms
from django.forms import fields
from . import models
from django.forms import widgets
# 倒入全局钩子函数
from django.core.exceptions import ValidationError


SEX = models.Sex.objects.all()
TYPE = models.StudentType.objects.all()
STATUS = models.StudentStatus.objects.all()


class RegisterOne(forms.Form):
    account_number = forms.CharField(label='用户名', widget=widgets.Input(
        attrs={'placeholder': '登陆后显示名称，大小写字母中文组合4-12位'}))
    username = forms.CharField(label='账号', widget=widgets.Input(
        attrs={'placeholder': '登陆验证账号，大小写字母开头，8-16位，不能包含除_之外特殊字符'}))
    password = forms.CharField(label='密码', widget=widgets.Input(
        attrs={'type': 'password','placeholder': '8-24位，大小写字母开头,字母和数字'}))
    repeat_password = forms.CharField(label='密码', widget=widgets.Input(
        attrs={'type': 'password', 'placeholder': '再次输入密码'}))
    email = forms.EmailField(label='邮箱', widget=widgets.Input(
        attrs={'placeholder': '可用于重置密码'}))
    tel = forms.CharField(label='手机号码', widget=widgets.Input(
        attrs={'id': 'id_student_tel', 'placeholder': '可用于重置密码'}))

    def clean(self):
        clean_d = False
        account_number = self.cleaned_data.get('account_number')
        pattern = r'([\u4e00-\u9fa5]|[a-zA-Z]){4,12}'
        if not account_number or not re.fullmatch(pattern, account_number):
            self.add_error('account_number', ValidationError('用户名不符合规范'))
            clean_d = True

        if models.RegisterFirst.objects.filter(account_number=account_number):
            self.add_error('account_number', '用户名已经存在')
            clean_d = True

        if len(account_number) > 12:
            self.add_error('account_number', '账号过长')
            clean_d = True

        if len(account_number) < 4:
            self.add_error('account_number', '账号过短')
            clean_d = True

        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('repeat_password')

        # 判断密码是否符合规范且两次密码是否一致
        pattern = r'^[A-Za-z][A-Za-z0-9]{7,23}'
        if not password or not re.fullmatch(pattern, password):
            self.add_error('password', ValidationError('密码不符合规范'))
            clean_d = True

        if re_password and re_password != password:
            self.add_error('repeat_password', ValidationError('两次密码不一致'))
            clean_d = True

        # 判断用户名是否符合规范
        username = self.cleaned_data.get('username')
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]{8,16}$'
        if not username or not re.fullmatch(pattern, username):
            self.add_error('username', '账号不符合规范')
            clean_d = True

        # 判断用户名是否已经存在
        if models.RegisterFirst.objects.filter(username=username):
            self.add_error('username', '用户名已经存在')
            clean_d = True

        # 判断电话号码是否符合规范
        telephone = self.cleaned_data.get('tel')
        pattern = r'^((13[0-9])|(14[5,7,9])|(15[^4])|(18[0-9])|(17[0,1,3,5,6,7,8]))\d{8}$'
        if not telephone or not re.fullmatch(pattern, telephone):
            self.add_error('tel', '电话号码不符合规范')
            clean_d = True

        if not clean_d:
            return self.cleaned_data


class RegisterThree(forms.Form):
    student_real_name = forms.CharField(label='姓名')
    student_id_card = forms.CharField(label='身份证')
    student_location_of_household_registration = forms.CharField(label='户口性质')
    student_tel_two = forms.CharField(label='第二联系人')
    student_address = forms.CharField(label='现居住地')
    student_registration_address = forms.CharField(label='户籍所在地')
    student_middle_school = forms.CharField(label='初中所在学校')
    student_high_school = forms.CharField(label='高中所在学校')
    student_sex = forms.ModelChoiceField(label='性别', empty_label='请选择', queryset=SEX)
    student_type = forms.ModelChoiceField(label='生源类型', empty_label='请选择', queryset=TYPE)

    def clean(self):
        clean_d = False

        student_high_school = self.cleaned_data.get('student_high_school')
        if len(student_high_school) > 64:
            self.add_error('student_high_school', ValidationError('输入过长'))
            clean_d = True

        student_middle_school = self.cleaned_data.get('student_middle_school')
        if len(student_middle_school) > 64:
            self.add_error('student_middle_school', ValidationError('输入过长'))
            clean_d = True

        student_registration_address = self.cleaned_data.get('student_registration_address')
        if len(student_registration_address) > 128:
            self.add_error('student_registration_address', ValidationError('输入过长'))
            clean_d = True

        student_address = self.cleaned_data.get('student_address')
        if len(student_address) > 128:
            self.add_error('student_address', ValidationError('输入过长'))
            clean_d = True

        student_location_of_household_registration = self.cleaned_data.get('student_location_of_household_registration')
        if len(student_location_of_household_registration) > 32:
            self.add_error('student_location_of_household_registration', ValidationError('输入过长'))
            clean_d = True

        student_real_name = self.cleaned_data.get('student_real_name')
        pattern = r'[\u4e00-\u9fa5]{2,4}'
        if not student_real_name or not re.fullmatch(pattern, student_real_name):
            self.add_error('student_real_name', ValidationError('姓名不符合规范'))
            clean_d = True

        pattern = r"(^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$)" \
                  r"|(^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$)"
        student_id_card = self.cleaned_data.get('student_id_card')
        if not student_id_card or not re.fullmatch(pattern, student_id_card):
            self.add_error('id_card', '身份证不符合规范')
            clean_d = True

        if len(student_id_card) > 18:
            self.add_error('id_card', '身份证超过18位')
            clean_d = True

        if len(student_id_card) < 15:
            self.add_error('id_card', '身份证低于15位')
            clean_d = True

        # 判断电话号码是否符合规范
        student_tel_two = self.cleaned_data.get('student_tel_two')
        pattern = r'^((13[0-9])|(14[5,7,9])|(15[^4])|(18[0-9])|(17[0,1,3,5,6,7,8]))\d{8}$'
        if not student_tel_two or not re.fullmatch(pattern, student_tel_two):
            self.add_error('student_tel_two', '电话号码不符合规范')
            clean_d = True

        if not clean_d:
            return self.cleaned_data
