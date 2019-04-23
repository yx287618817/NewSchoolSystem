import base64
import os
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

from django.db import models


class ImageTest(models.Model):
    img = models.BinaryField()

# ------------------------------------------- 用户表 ---------------------------------------------------


class UserMessage(models.Model):
    """
    保存用户头像和身份证明
    """
    photo = models.ImageField(verbose_name='头像', null=True, unique=False)
    card_id = models.CharField(verbose_name='账号', max_length=32, unique=True)

    def __str__(self):
        return self.card_id


# ------------------------------------------- 用户表 ---------------------------------------------------


# class Teachers(models.Model):
#     """
#     老师表
#     """
#     teacher_name = models.CharField('姓名', max_length=32)


class RegisterFirst(models.Model):
    """
    注册第一页
    """
    file = os.path.join(os.getcwd(), 'statics', 'USER_DEFAULT_PHOTO.png')
    with open(file, 'rb') as f1:
        DEFAULT_PHOTO = f1.read()

    student_account_number = models.CharField(verbose_name='用户名', max_length=13, unique=True)
    student_number = models.CharField(verbose_name='学号', max_length=13, unique=True)
    student_username = models.CharField(verbose_name='账号', max_length=32, unique=True, null=True)
    student_password = models.CharField(verbose_name='密码', max_length=32, default='123456')
    student_email = models.EmailField(verbose_name='邮箱')
    student_tel = models.CharField(verbose_name='学生电话', max_length=15)
    student_register_date = models.DateField(verbose_name='注册时间')
    student_group = models.ForeignKey('Group', verbose_name='用户组', on_delete=models.CASCADE, default=1)
    register_one_status = models.BooleanField(verbose_name='第一步信息是否已经完成', default=0)
    user_photo = models.BinaryField(verbose_name='用户头像', default=DEFAULT_PHOTO)

    def __str__(self):
        return self.student_username

    class Meta:
        ordering = ['id']
        verbose_name = '学生注册信息'
        verbose_name_plural = verbose_name


class RegisterTwo(models.Model):
    """
        主专业分类
    """
    first = models.ForeignKey('RegisterFirst', verbose_name='用户', on_delete=models.CASCADE)
    major_child = models.ForeignKey('MajorChild', verbose_name='专业选择', on_delete=models.CASCADE)
    status = models.BooleanField('主专业', default=0)
    register_two_status = models.BooleanField('第二步信息是否已经完成', default=0)

    def __str__(self):
        return '%s ==> %s' % (self.major_child.caption, self.major_child.major.caption)

    class Meta:
        unique_together = ['first', 'major_child']
        ordering = ['status']
        verbose_name = '学生专业关系'
        verbose_name_plural = verbose_name


class RegisterThree (models.Model):
    first = models.ForeignKey('RegisterFirst', verbose_name='用户', on_delete=models.CASCADE)
    student_real_name = models.CharField('姓名', max_length=32)
    # student_photo = models.ImageField('头像')
    student_id_card = models.CharField('身份证', max_length=18)
    student_location_of_household_registration = models.CharField('户口性质', max_length=32)
    student_tel_two = models.CharField('第二联系人', max_length=15)
    student_address = models.CharField('现居住地', max_length=128)
    student_registration_address = models.CharField('户籍所在地', max_length=128)
    student_middle_school = models.CharField('初中所在学校', max_length=18)
    student_high_school = models.CharField('高中所在学校', max_length=18)
    student_sex = models.ForeignKey('Sex', verbose_name='性别', on_delete=models.CASCADE)
    student_type = models.ForeignKey('StudentType', verbose_name='生源类型', on_delete=models.CASCADE)
    student_status = models.ForeignKey('StudentStatus', verbose_name='生源状态', on_delete=models.CASCADE, default=1,)
    register_three_status = models.BooleanField('第三步信息是否已经完成', default=0)

    def __str__(self):
        return self.two.first.student_username

    class Meta:
        ordering = ['id']
        verbose_name = '重要信息'
        verbose_name_plural = verbose_name

# ------------------------------------------- 通用多选 ---------------------------------------------------


class Sex(models.Model):
    """
    状态
    """
    sex = models.CharField(verbose_name='性别', max_length=10, unique=True)

    def __str__(self):
        return self.sex

    class Meta:
        verbose_name = '性别管理'
        verbose_name_plural = verbose_name


# ------------------------------------------- 班级年级多选 ---------------------------------------------------


class Grades(models.Model):
    """班级表"""
    grade_name = models.CharField('年级名称', max_length=32, unique=True)

    def __str__(self):
        return self.grade_name

    class Meta:
        verbose_name = '年级管理'
        verbose_name_plural = verbose_name


class Classes(models.Model):
    """
    班级表
    """
    class_name = models.CharField('班级名称', max_length=32, unique=True)

    def __str__(self):
        return self.class_name

    class Meta:
        verbose_name = '班级管理'
        verbose_name_plural = verbose_name


class ClassSelect(models.Model):
    grade_name = models.ForeignKey('Grades', on_delete=models.CASCADE, verbose_name='年级名称')
    class_name = models.ForeignKey('Classes', on_delete=models.CASCADE, verbose_name='班级名称')

    def __str__(self):
        return '%s ===> %s' % (self.grade_name.grade_name, self.class_name.class_name)

    class Meta:
        unique_together = ['grade_name', 'class_name']
        verbose_name = '班级分配'
        verbose_name_plural = verbose_name


# ------------------------------------------- 学生多选 ---------------------------------------------------


class StudentStatus(models.Model):
    """
    状态
    """
    student_status = models.CharField(verbose_name='学生状态', max_length=10, unique=True)

    def __str__(self):
        return self.student_status

    class Meta:
        verbose_name = '学生状态管理'
        verbose_name_plural = verbose_name


class StudentType(models.Model):
    """
    生源管理
    """
    student_type = models.CharField('生源类型', max_length=32, unique=True)

    def __str__(self):
        return self.student_type

    class Meta:
        verbose_name = '生源类型管理'
        verbose_name_plural = verbose_name


# ------------------------------------------- 学生多选 ---------------------------------------------------


class Major(models.Model):
    """
    专业管理
    """
    image = models.ImageField(verbose_name='专业对应图片')
    caption = models.CharField('专业', max_length=32, unique=True)

    def __str__(self):
        return self.caption

    class Meta:
        ordering = ['caption']
        verbose_name = '专业管理'
        verbose_name_plural = verbose_name


class MajorChild(models.Model):
    major = models.ForeignKey('Major', on_delete=models.CASCADE)
    caption = models.CharField('专业细分', max_length=32, unique=True)

    def __str__(self):
        return '%s ==> %s' % (self.major.caption, self.caption)

    class Meta:
        ordering = ['major']
        verbose_name = '专业细分'
        verbose_name_plural = verbose_name


# ------------------------------------------- 权限管理 ---------------------------------------------------


# 无需权限验证表
class NoPermission(models.Model):
    caption = models.CharField(max_length=32, verbose_name='无需权限验证', unique=True)

    def __str__(self):
        return self.caption

    class Meta:
        ordering = ['caption']
        verbose_name = '无需权限验证的路径'
        verbose_name_plural = verbose_name


"""
    权限管理表
    1.创建用户组
    2.用户注册,默认初始用户组
"""


# 用户表
class User(models.Model):
    """
        用户信息表
    """
    userName = models.CharField(max_length=32, verbose_name='学生姓名', unique=True)
    password = models.CharField(max_length=128, verbose_name='密码')
    # email = models.EmailField(verbose_name='邮箱')
    # telephone = models.CharField(max_length=18, verbose_name='手机号')

    class Meta:
        ordering = ['userName']
        verbose_name = '1-创建用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.userName


# 用户组表
class Group(models.Model):
    """
        用户组管理
    """
    groupName = models.CharField(max_length=32, verbose_name='用户组', unique=True)

    class Meta:
        ordering = ['groupName']
        verbose_name = '2-创建用户组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.groupName


# 用户分配用户组
class UserGroup(models.Model):
    """
        用户分配用户组：用户和用户组间关系
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)

    class Meta:
        ordering = ['group']
        verbose_name = '3-用户分配用户组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s ---> %s" % (self.user.userName, self.group.groupName)


# 权限表
class Permission(models.Model):
    """
        权限管理
    """
    tableName = models.ForeignKey('TableName', on_delete=models.CASCADE)
    tablePermission = models.ForeignKey('TablePermission', on_delete=models.CASCADE)

    class Meta:
        ordering = ['tableName']
        verbose_name = '6-设置表权限'
        verbose_name_plural = verbose_name
        unique_together = ['tablePermission', 'tableName']

    def __str__(self):
        return '%s ---> %s' % (self.tableName.caption, self.tablePermission.caption)


# 操作表权限
class TablePermission(models.Model):
    """
        所有表路径
    """
    caption = models.CharField(max_length=32, verbose_name='操作名称', unique=True)
    tableUrl = models.CharField(max_length=128, verbose_name='操作路径', unique=True)

    class Meta:
        ordering = ['caption']
        verbose_name = '5-数据表操作'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.caption, self.tableUrl)


# 操作表
class TableName(models.Model):
    """
        所有需要操作的数据表
    """
    caption = models.CharField(max_length=128, verbose_name='设置需要操作数据表', unique=True)
    tableName = models.CharField(max_length=128, verbose_name='数据表路径', unique=True)

    class Meta:
        ordering = ['caption']
        verbose_name = '4-设置需要操作数据表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.caption


# 用户组分配权限
class GroupPermission(models.Model):
    """
        用户组分配权限
    """
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    permission = models.ForeignKey('Permission', on_delete=models.CASCADE)

    class Meta:
        ordering = ['group']
        verbose_name = '7-用户组分配权限'
        verbose_name_plural = verbose_name
        unique_together = ['group', 'permission']

    def __str__(self):
        """
            管理员 ==> 学生表：更新: student/update/
        """
        return '%s ---> %s表: %s: %s/%s/' % (
            self.group.groupName, self.permission.tableName.tableName,
            self.permission.tablePermission.caption, self.permission.tableName.tableName,
            self.permission.tablePermission.tableUrl)
