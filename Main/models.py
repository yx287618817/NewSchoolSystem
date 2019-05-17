import base64
import os
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

from django.db import models


# 密码加盐
class HashlibSalt(models.Model):
    salt = models.CharField(max_length=300, verbose_name='加盐')

# ------------------------------------------- 用户表 ---------------------------------------------------


class RegisterThree (models.Model):
    first = models.ForeignKey('RegisterFirst', verbose_name='用户', on_delete=models.CASCADE)
    student_real_name = models.CharField('姓名', max_length=32)
    student_id_card = models.CharField('身份证', max_length=18)
    student_location_of_household_registration = models.CharField('户口性质', max_length=32)
    student_tel_two = models.CharField('第二联系人', max_length=15)
    student_address = models.CharField('现居住地', max_length=128)
    student_registration_address = models.CharField('户籍所在地', max_length=128)
    student_middle_school = models.CharField('初中所在学校', max_length=18)
    student_high_school = models.CharField('高中所在学校', max_length=18)
    student_sex = models.ForeignKey('Sex', verbose_name='性别', on_delete=models.CASCADE)
    student_type = models.ForeignKey('StudentType', verbose_name='生源类型', on_delete=models.CASCADE)
    student_status = models.ForeignKey('StudentStatus', verbose_name='生源状态', on_delete=models.CASCADE, default=2,)
    register_three_status = models.BooleanField('第三步信息是否已经完成', default=0)

    def __str__(self):
        return self.student_real_name

    class Meta:
        ordering = ['id']
        verbose_name = '重要信息'
        verbose_name_plural = verbose_name


class RegisterFirst(models.Model):
    """
    注册第一页
    """
    file = os.path.join(os.getcwd(), 'statics', 'USER_DEFAULT_PHOTO.jpeg')
    with open(file, 'rb') as f1:
        DEFAULT_PHOTO = f1.read()

    account_number = models.CharField(verbose_name='用户名', max_length=13, unique=True)
    number = models.CharField(verbose_name='学号', max_length=13, unique=True)
    username = models.CharField(verbose_name='账号', max_length=32, unique=True, null=True)
    password = models.CharField(verbose_name='密码', max_length=300)
    email = models.EmailField(verbose_name='邮箱')
    tel = models.CharField(verbose_name='学生电话', max_length=15)
    register_date = models.DateField(verbose_name='注册时间')
    register_one_status = models.BooleanField(verbose_name='第一步信息是否已经完成', default=0)
    user_photo = models.BinaryField(verbose_name='用户头像', default=DEFAULT_PHOTO)
    user_salt = models.ForeignKey('HashlibSalt', verbose_name='盐', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.username

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
    caption = models.CharField('专业细分', max_length=32, null=True, blank=True)

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
# class User(models.Model):
#     """
#         用户信息表
#     """
#     userName = models.CharField(max_length=32, verbose_name='学生姓名', unique=True)
#     password = models.CharField(max_length=128, verbose_name='密码')
#     # email = models.EmailField(verbose_name='邮箱')
#     # telephone = models.CharField(max_length=18, verbose_name='手机号')
#
#     class Meta:
#         ordering = ['userName']
#         verbose_name = '1-创建用户'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.userName


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
    tableUrl = models.CharField(max_length=128, verbose_name='操作路径', unique=True, null=True, blank=True)

    class Meta:
        ordering = ['caption']
        verbose_name = '5-数据表操作'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.caption


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
        return '%s ---> %s: %s' % (
            self.group.groupName, self.permission.tableName.caption,
            self.permission.tablePermission.caption)


# 用户分配用户组
class UserGroup(models.Model):
    """
        用户分配用户组：用户和用户组间关系
    """
    user = models.ForeignKey('RegisterFirst', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)

    class Meta:
        ordering = ['group']
        unique_together = ['user', 'group']
        verbose_name = '3-用户分配用户组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s ---> %s" % (self.user.username, self.group.groupName)


# *********************************************************************************
# *********************************************************************************
# *********************************************************************************



# 年级表
class Grade(models.Model):
    grade_name = models.CharField(max_length=128, unique=True, verbose_name='班级名称')
    department = models.ForeignKey('Major', on_delete=models.CASCADE, verbose_name='班级所在系部')
    course = models.ManyToManyField('Course', verbose_name='课程与班级')
    teacher = models.ManyToManyField('RegisterFirst', verbose_name='班级对应教师')

    def __str__(self):
        return '%s' % self.grade_name

    class Meta:
        verbose_name = '班级表'
        verbose_name_plural = verbose_name


class Course(models.Model):
    course_name = models.CharField(max_length=128, unique=True, verbose_name='课程名字')

    def __str__(self):
        return '%s' % self.course_name

    class Meta:
        verbose_name = '课程表'
        verbose_name_plural = verbose_name



class DepToTea(models.Model):
    department = models.ForeignKey('Major', on_delete=models.CASCADE, verbose_name="对应部门表")
    teacher = models.ForeignKey('RegisterFirst', on_delete=models.CASCADE, verbose_name="对应教师")

    def __str__(self):
        return '%s --> %s' % (self.department_id, self.teacher_id)

    class Meta:
        verbose_name = '部门对应老师'
        verbose_name_plural = verbose_name


# 编写账户类型表, 存放所有账户的类型
class Account_type(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(verbose_name='账户类型',max_length=128, unique=True)

    def __str__(self):
        return '%s' % self.type_name

    class Meta:
        verbose_name = '账户类型'
        verbose_name_plural = verbose_name


class Education(models.Model):
    id = models.AutoField(primary_key=True)
    education = models.CharField(max_length=128, verbose_name='学历', unique=True)

    def __str__(self):
        return self.education

    class Meta:
        verbose_name = '学历'
        verbose_name_plural = verbose_name

class ZhiCheng(models.Model):
    id = models.AutoField(primary_key=True)
    call = models.CharField(max_length=64, unique=True, verbose_name='职称')

    def __str__(self):
        return self.call

    class Meta:
        verbose_name = '职称'
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    user_id = models.AutoField(primary_key=True)
    real_name = models.CharField(verbose_name='姓名',max_length=16)
    gender = models.ForeignKey('Sex', on_delete=models.CASCADE, verbose_name='性别')
    birth = models.DateField(verbose_name='出生日期')
    acc_type = models.ForeignKey('Account_type', to_field='id', on_delete=models.CASCADE,verbose_name='账户类型', default='3')
    education = models.ForeignKey('Education', to_field='id', on_delete=models.CASCADE, verbose_name='学历')
    call = models.ForeignKey('ZhiCheng', to_field='id', on_delete=models.CASCADE, verbose_name='职称')
    address = models.CharField(max_length=256, verbose_name='家庭地址')

    def __str__(self):
        return '%s' % self.real_name

    class Meta:
        verbose_name = '教师用户'
        verbose_name_plural = verbose_name


class Work_type(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(verbose_name='工作类型',max_length=64)

    def __str__(self):
        return '%s' % self.type_name

    class Meta:
        verbose_name = '工作类型'
        verbose_name_plural = verbose_name


class Work_state(models.Model):
    id = models.AutoField(primary_key=True)
    state_name = models.CharField(verbose_name='工作状态',max_length=64)

    def __str__(self):
        return '%s' % self.state_name

    class Meta:
        verbose_name = '工作状态'
        verbose_name_plural = verbose_name


# 时间,系部,教师名字/id,标题,内容,工作状态,工作类型(日/周/月)
class Work_arrange(models.Model):
    #  主键查询
    id = models.AutoField(primary_key=True)
    # 部门用来表示是哪个部门的工作,
    department = models.ForeignKey('Major', to_field='id',on_delete=models.CASCADE, verbose_name='部门', max_length=64)
    # 表示给这个部门的某个教师分配的工作
    tea_id = models.ForeignKey('RegisterFirst', on_delete=models.CASCADE,verbose_name='对应教师')
    # 工作标题
    title = models.CharField(verbose_name='工作标题',max_length=512)
    # 工作内容
    content = models.CharField(verbose_name='工作内容',max_length=4096)
    # 工作类型(日/周/月)
    work_type = models.ForeignKey('Work_type', to_field='id', on_delete=models.CASCADE,verbose_name='工作类型')
    # 工作状态,
    work_state = models.ForeignKey('Work_state', to_field='id', on_delete=models.CASCADE,verbose_name='工作状态')
    # 工作任务生成时间
    date = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)
    # 工作完成时间
    finish = models.DateTimeField(verbose_name='完成时间记录最后一次修改数据的时间', auto_now=True)

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = '工作安排'
        verbose_name_plural = verbose_name

# 保存数据库格式: 工作标题,完成人,完成时间,备注.


class Inform(models.Model):
    id = models.AutoField(primary_key=True)
    send_from_tea = models.ForeignKey('RegisterFirst', related_name='from_teacher', on_delete=models.CASCADE, verbose_name='来自')
    send_to_tea = models.ForeignKey('RegisterFirst',related_name='to_teacher', on_delete=models.CASCADE, verbose_name='发送给哪个教师')
    title = models.CharField(max_length=128)
    content = models.TextField()
    filed_name = models.CharField(max_length=128, verbose_name='上传文件的文件名', null=True, blank=True)
    local_file = models.CharField(max_length=128, verbose_name='保存到本地的文件名', null=True, blank=True)
    times = models.DateField(auto_now_add=True, verbose_name='发布时间')
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = '消息通知'
        verbose_name_plural = verbose_name
