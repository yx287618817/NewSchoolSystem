import base64
import datetime
import hashlib
import json
import random
import re
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from . import models
from functools import wraps
from . import Smsverification as c


# 短信验证
def code_verification(req):
    client = c.ZhenziSmsClient(
        'https://sms_developer.zhenzikj.com',
        '101373',
        '841e3458-a590-4347-88e6-bc64e8cdb25b')
    code = ''
    tel = req.POST.get('tel')
    for _ in range(6):
        code += str(random.randint(0, 9))
    result = client.send(tel, '感谢您使用Awesome教务管理系统。您的验证码是：%s' % code)
    result = json.loads(result)
    if result['data'] == '发送成功':
        req.session['code_vfi'] = code
        return True
    return False


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
        salt = models.RegisterFirst.objects.filter(username=username).values_list('user_salt__salt').first()[0]
    except Exception:
        return False
    p = hashlib.sha256()
    p.update(bytes(password + salt, encoding='utf-8'))
    pwd = p.hexdigest()
    if models.RegisterFirst.objects.filter(username=username, password=pwd).first():
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
        username=username).first().user_photo
    img = base64.b64encode(img).decode()
    return img


def write_session(req, username):
    req.session['username'] = username
    req.session['number'] = models.RegisterFirst.objects.filter(
        username=username).values_list('number').first()[0]
    req.session['account_number'] = models.RegisterFirst.objects.filter(
        username=username).values_list('account_number').first()[0]
    req.session['user_photo'] = get_user_photo(username=username)


# 用户登陆，判断信息是否完整
def is_register(req):
    if req.POST.get('password', None) and req.POST.get('username', None):
        # POST方式提交登陆请求
        username = req.POST.get('username', None)
        password = req.POST.get('password', None)
        # 如果用户登陆验证通过
        if verification_pwd(username, password):
            write_session(req, username)
        else:
            return HttpResponse("<script>alert('账号密码错误');location.href='/';</script>")
    else:
        # 已经登录
        username = req.session.get('username')
        if not username:
            return render(req, 'login.html')

    group = list(models.RegisterFirst.objects.filter(
        username=username).values_list('usergroup__group__groupName'))

    group_name_list = [j for i in group for j in i]

    number = models.RegisterFirst.objects.filter(username=username).first().number

    if '管理员' in group_name_list:
        return HttpResponseRedirect('/back_manage/')

    if 'TC' in number:
        return HttpResponseRedirect('/teacher_manage/')

    if 'ST' in number:
        try:
            models.RegisterTwo.objects.filter(
                first__username=username).values_list('register_two_status').first()[0]
        except Exception:
            return HttpResponse("<script>alert('请完善您的专业信息');location.href='/register_two/';</script>")
        else:
            # 判断详细信息是否完善
            try:
                models.RegisterThree.objects.filter(
                    first__username=username).values_list('register_three_status').first()[0]
            except Exception:
                return HttpResponse("<script>alert('请完善您的个人信息');location.href='/register_three/';</script>")
            else:
                return HttpResponseRedirect('/student_menu/')
    else:
        return HttpResponseRedirect('/teacher_menu/')


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

    # @staticmethod
    # def make_user():
    #     user = [('胡宇', '123'), ('魏婷', '123'), ('贺奕', '123'), ('杜凌风', '123'),
    #             ('杨真', '123'), ('袁雄', '123'), ('刘刚', '123')]
    #     for i in user:
    #         models.User.objects.create(
    #             userName=i[0],
    #             password=i[1]
    #         )

    @staticmethod
    def make_group():
        group = ['意向学生', '意向教师', '管理员']
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
    def make_type():
        models.StudentType.objects.create(type='统招')
        models.StudentType.objects.create(type='艺考')
        models.StudentType.objects.create(type='特长生')
        models.StudentType.objects.create(type='成考')

    @staticmethod
    def make_status():
        models.StudentStatus.objects.create(status='注册')
        models.StudentStatus.objects.create(status='在校')
        models.StudentStatus.objects.create(status='毕业')
        models.StudentStatus.objects.create(status='退学')

    @staticmethod
    def make_no_permission():
        models.NoPermission.objects.create(caption='/menu/')
        models.NoPermission.objects.create(caption='/register_one/')
        models.NoPermission.objects.create(caption='/register_two/')
        models.NoPermission.objects.create(caption='/register_three/')


# 生成学生学号
def get_card_id():
    sr = 'ST' + '-' + str(datetime.datetime.now()).split(' ')[0].replace('-', '')[2:] \
         + str(random.randint(1000, 9999))
    if models.RegisterFirst.objects.filter(number=sr).first():
        return get_card_id()
    return sr


# 生成教师编号
def get_tc_card_id():
    sr = 'TC' + '-' + str(datetime.datetime.now()).split(' ')[0].replace('-', '')[2:] \
         + str(random.randint(1000, 9999))
    if models.RegisterFirst.objects.filter(number=sr).first():
        return get_tc_card_id()
    return sr


# re判断是否有权限
def is_get_permission(permission_list, path):
    for i in permission_list:
        sr = r'^%s(\?[a-zA-Z]+=[0-9]+(&[a-zA-Z]+=[0-9]+)?)?' % i
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
            return HttpResponse("<script>alert('登陆身份验证失败,请重新登陆');location.href='/';</script>")
        # 判断是否有权限,如果没有权限则不执行后面的操作,返回‘没有权限’
        permission_list = get_permission(username)
        if is_get_permission(permission_list, req.path):
            result = function(req, *args)
            try:
                return result
            except Exception as e:
                print(e)
                HttpResponse("<script>alert('出错了');location.href='%s';</script>" % req.path)
        req.session.clear()
        return HttpResponse("<script>alert('您没有权限');location.href='/';</script>")
    return inner


# 获取权限列表
def get_permission(username):
    permission_list = []
    groups =[i for j in list(models.UserGroup.objects.filter(
        user__username=username).values_list('group__groupName')) for i in j]

    for group in groups:
        p = list(models.GroupPermission.objects.filter(group__groupName=group).values_list(
            'permission__tableName__tableName', 'permission__tablePermission__tableUrl'))
        lst = [(i[0] + i [1]) if i[1] else i[0] for i in p]
        permission_list.extend(lst)
    # 生成权限列表
    permission_list = list(set(permission_list))
    return permission_list


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
            html += '<div class="menu">'
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
