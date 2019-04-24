import base64
import datetime
import hashlib
import random
import re
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from . import models
from functools import wraps


#  注册密码加盐加密，并将盐存入数据库与用户建立关系
def get_hashlib_salt(pwd):
    salt = ''
    for _ in range(random.randint(10, 100)):
        a = random.randint(65, 90)
        b = random.randint(97, 122)
        salt += (chr(a) + chr(b))
    s = hashlib.sha256()
    s.update(bytes(salt, encoding='utf-8'))
    salt = s.hexdigest()
    p = hashlib.sha256()
    p.update(bytes(pwd + salt, encoding='utf-8'))
    pwd = p.hexdigest()
    return pwd, salt


# 登陆时取用户盐进行验证
def verification_pwd(username, password):
    # 出错说明没有此用户
    try:
        salt = models.RegisterFirst.objects.filter(student_username=username).values_list('user_salt__salt').first()[0]
    except Exception:
        return False
    p = hashlib.sha256()
    p.update(bytes(password + salt, encoding='utf-8'))
    pwd = p.hexdigest()
    if models.RegisterFirst.objects.filter(student_username=username, student_password=pwd).first():
        return True
    else:
        return False


# 转换二进制图片文件
def get_user_photo(username):
    """
    前端显示<input type="image" src="data:image/jpeg;base64,{{ img }}">
    :return:
    """
    img = models.RegisterFirst.objects.filter(
        student_username=username).first().user_photo
    img = base64.b64encode(img).decode()
    return img


def write_session(req, username):
    req.session['username'] = username
    req.session['number'] = models.RegisterFirst.objects.filter(
        student_username=username).values_list('student_number').first()[0]
    req.session['account_number'] = models.RegisterFirst.objects.filter(
        student_username=username).values_list('student_account_number').first()[0]
    req.session['user_photo'] = get_user_photo(username=username)


# 用户登陆，判断信息是否完整
def is_student_register(req):
    if req.POST.get('password', None) and req.POST.get('username', None):
        # POST方式提交登陆请求
        username = req.POST.get('username', None)
        password = req.POST.get('password', None)
        # 如果用户登陆验证通过
        if verification_pwd(username, password):
            write_session(req, username)
        else:
            return HttpResponse("<script>alert('账号密码错误');location.href='/student_login/';</script>")
    else:
        username = username = req.session.get('username')
        if not username:
            return render(req, 'student_login.html')

    try:
        models.RegisterTwo.objects.filter(
            first__student_username=username).values_list('register_two_status').first()[0]
    except Exception:
        return HttpResponse("<script>alert('请完善您的专业信息');location.href='/register_two/';</script>")
    else:
        # 判断详细信息是否完善
        try:
            models.RegisterThree.objects.filter(
                first__student_username=username).values_list('register_three_status').first()[0]
        except Exception:
            return HttpResponse("<script>alert('请完善您的个人信息');location.href='/register_three/';</script>")
        else:
            return HttpResponseRedirect('/student_menu/')


# 删除库时默认生成测试数据
class GetManage(object):
    """
        删库时生成测试数据的配置文件
    :return:
    """
    @staticmethod
    def make_major():
        
        major = [('4.png', '哲学类'), ('5.png', '经济学'), ('6.png', '法学类'),
                 ('7.png', '教育类'), ('8.png', '文学类'), ('9.png', '历史学类'), 
                 ('10.png', '理学类'), ('11.png', '农学类'), ('12.png', '医学类'), 
                 ('13.png', '管理类'), ('14.png', '艺术类'), ('15.png', '军事类'), ('16.png', '工学类')]
            
        for i in major:
            models.Major.objects.create(image=i[0], caption=i[1])

        major_child = [
            ('逻辑学', '哲学', '宗教学'),
            ('财政学', '金融学', '经济贸易'),
            ('法学', '政治行政学', '社会学', '公安学', '民族学', '马克思主义理论'),
            ('教育学', '科学教育', '人文教育', '教育技术', '学前教育', '小学教育', '特殊教育', '体育教育'),
            ('中国语言文学', '外国语言文学', '新闻传播学'),
            ('历史学', '世界史', '考古学', '文物与博物馆学'),
            ('数学', '物理学', '化学', '天文学', '地理学', '大气学', '海洋学', '地理物理', '生物科学', '地质学', '统计学'),
            ('植物生产', '草学类', '动物生产', '林业学', '水产学', '自然保护与环境生态'),
            ('基础医学', '临床医学', '口腔医学', '中西医学', '中医学', '中药学', '法医学', '医学技术', '护理学', '公共卫生与预防医学'),
            ('管理科学与工程', '农业经济管理', '图书情报与档案管理', '电子商务', '旅游管理', '工商管理', '物理管理与工程'),
            ('艺术理论学', '戏剧与影视学', '音乐与舞蹈学', '美术学', '设计学'),
            ('军事思想与军事理论', '战役学', '军事后勤与军事装备', '战略学', '军制学', '军队指挥', '战术类'),
            ('力学', '机械学', '仪器学', '材料学', '电气学', '自动化', '核工程', '能源动力', '建筑学', '电子信息工程', '生物工程')]

        i = 1
        for j in major_child:
            for z in j:
                models.MajorChild.objects.create(
                    caption=z,
                    major_id=i)
            i += 1

    @staticmethod
    def make_user():
        user = [('胡宇', '123'), ('魏婷', '123'), ('贺奕', '123'), ('杜凌风', '123'),
                ('杨真', '123'), ('袁雄', '123'), ('刘刚', '123')]
        for i in user:
            models.User.objects.create(
                userName=i[0],
                password=i[1]
            )

    @staticmethod
    def make_group():
        group = ['学生', '老师', '管理员']
        for i in group:
            models.Group.objects.create(
                groupName=i
            )

    @staticmethod
    def make_user_group():
        user_group = [(1, 1), (2, 2), (3, 1), (4, 2), (5, 2), (6, 3), (7, 1)]
        for i in user_group:
            models.UserGroup.objects.create(
                user_id=i[0],
                group_id=i[1]
            )

    @staticmethod
    def make_table():
        table = [('学生信息表', 'student'), ('教师信息表', 'teacher')]
        for i in table:
            models.TableName.objects.create(caption=i[0], tableName=i[1])

    @staticmethod
    def make_table_permission():
        table_permission = [
            ('删除', 'delete'), ('删除单个信息', 'delete_one'),
            ('增加', 'add'), ('增加单个信息', 'add_one'),
            ('更新', 'update'), ('更新单个信息', 'update_one'),
            ('查询', 'select'), ('查询单个信息', 'select_one'),
        ]
        for i in table_permission:
            models.TablePermission.objects.create(
                caption=i[0],
                tableUrl=i[1])

    @staticmethod
    def make_permission():
        permission = [
            (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
            (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8)
        ]
        for i in permission:
            models.Permission.objects.create(tableName_id=i[0], tablePermission_id=i[1])

    @staticmethod
    def make_group_permission():
        group_permission = [
            (1, 4), (1, 6), (2, 3), (2, 5), (2, 12), (2, 14), (3, 1), (3, 2),
            (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10),
            (3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (3, 16)
        ]
        for i in group_permission:
            models.GroupPermission.objects.create(
                group_id=i[0],
                permission_id=i[1]
            )

    @staticmethod
    def make_sex():
        models.Sex.objects.create(sex='男')
        models.Sex.objects.create(sex='女')
        models.Sex.objects.create(sex='保密')

    @staticmethod
    def make_student_type():
        models.StudentType.objects.create(student_type='统招')
        models.StudentType.objects.create(student_type='艺考')
        models.StudentType.objects.create(student_type='特长生')
        models.StudentType.objects.create(student_type='成考')

    @staticmethod
    def make_student_status():
        models.StudentStatus.objects.create(student_status='注册')
        models.StudentStatus.objects.create(student_status='在校')
        models.StudentStatus.objects.create(student_status='毕业')
        models.StudentStatus.objects.create(student_status='退学')

    @staticmethod
    def make_no_permission():
        models.NoPermission.objects.create(caption='/student_menu/')
        models.NoPermission.objects.create(caption='/register_one/')
        models.NoPermission.objects.create(caption='/register_two/')
        models.NoPermission.objects.create(caption='/register_three/')


# 生成学生学号
def get_student_card_id():
    sr = 'ST' + '-' + str(datetime.datetime.now()).split(' ')[0].replace('-', '')[2:] \
         + str(random.randint(1000, 9999))
    if models.RegisterFirst.objects.filter(student_number=sr).first():
        return get_student_card_id()
    return sr


# re判断是否有权限
def is_get_permission(permission_list, path):
    for i in permission_list:
        sr = r'^%s(\?[a-zA-Z]+=[0-9]+)?/$' % i[:-1]
        try:
            re.match(sr, path).group()
        except Exception:
            pass
        else:
            return True
    return False


# 无需权限可以登陆的路径判断
def not_permission():
    not_permission_list = []
    for i in list(models.NoPermission.objects.all().values_list('caption')):
        not_permission_list.append(i[0])
    return not_permission_list


# 判断是否已经登陆以及是否有登陆权限
def is_login(function):
    @wraps(function)
    def inner(req, *args, **kwargs):
        username = req.session.get('username', None)
        if not username:
            return HttpResponse("<script>alert('登陆身份验证失败,请重新登陆');location.href='/student_login/';</script>")
        # 判断登陆身份，如果不是在校生则不让用户进入
        one = models.RegisterFirst.objects.filter(
            student_username=username).values(
            'registerthree__register_three_status').first()['registerthree__student_status__student_status']
        if one != '在校':
            return HttpResponse('<script>alert("Sorry，您不是在校学生，将跳转首页");location.href="/";</script>')
        # 这里应该修改成用正则表达式匹配
        # 判断是否有权限,如果没有权限则不执行后面的操作,返回‘没有权限’
        permission_list, permission_dict = get_permission(req.session.get('username', None),
                                                          login_type=req.session.get('login_who'))
        if is_get_permission(permission_list, req.path):
            result = function(req, *args)
            return result
        return HttpResponse("<script>alert('您没有权限');location.href='/';</script>")
    return inner


# 获取权限并生成权限字典
def get_permission(username, req):
    """
        接受用户姓名,返回权限列表作判断是否有权限,返回权限列表字典作显示
        :param username:
        :return: permission_list, permission_dict
    """
    permission_list = []
    permission_dict = {}
    group_list = list(models.RegisterFirst.objects.filter(
        student_username=username).values_list('student_group__groupName'))
    for group in group_list:
        permission_lst = list(models.Permission.objects.filter(
            grouppermission__group__groupName=group[0]).values_list(
            'tableName__tableName', 'tablePermission__tableUrl',
            'tableName__caption', 'tablePermission__caption'
        ))
        for i in permission_lst:
            permission = '/' + i[0] + '/' + i[1] + '/'
            permission_name = i[2] + ': ' + i[3]
            if i[2] not in permission_dict:
                permission_dict[i[2]] = [{'permission_name': permission_name, 'permission': permission}]
            else:
                if {'permission_name': permission_name, 'permission': permission} not in permission_dict[i[2]]:
                    permission_dict[i[2]].append({'permission_name': permission_name, 'permission': permission})
            if permission not in permission_list:
                permission_list.append(permission)
    return permission_list, permission_dict


# 生成权限显示html
def get_permission_html(permission_dict):
    """
    传入权限字典,生成html内容
    :param permission_dict: 权限字典
    :return: html
    """
    html = ''
    count = 0
    a = list(permission_dict.keys())
    a.sort()
    for k in a:
        if count == 3:
            count = 0
        if count == 0:
            html += '<div class="student_menu">'
        sr = '''
        <ul class ="permission_ul" >
            <li class ="parent" > %s </li>
        ''' % k
        for dic in permission_dict[k]:
            sr += '<li class ="child" > <a href="%s" > %s </a></li>' % (
                dic['permission'], dic['permission_name'])
        sr += '</ul>'
        html += sr
        count += 1
        if count == 3:
            html += '</div>'
    return html
