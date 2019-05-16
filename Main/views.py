import hashlib
import json
from django.db import transaction
from .get_result import *
from . import models
from functools import wraps
from . import myforms
import base64
from django.views.decorators.csrf import csrf_exempt
from .teacher.views import locked


@is_login
@locked
def student_announcement(request):
    return render(request, 'student_announcement.html')


@is_login
@locked
def student_course(request):
    return render(request, 'student_course.html')


@is_login
@locked
def student_leave(request):
    return render(request, 'student_leave.html')


@is_login
@locked
def student_performance(request):
    return render(request, 'student_announcement.html')


@is_login
@locked
def student_record(request):
    return render(request, 'student_announcement.html')


@is_login
@locked
def forget_passwd(request):
    if request.method == 'GET':
        request.session.clear()
        # 假如get方式登录
        verifi_sr = request.GET.get('verification_str')
        username = request.GET.get('username')
        if verifi_sr == 'verification_username':
            obj = models.RegisterFirst.objects.filter(username=username)
            if obj:
                # 有用户存在的情况下, ajax请求返回true否则返回false
                data = json.dumps({'verification_username_result': 'true'})
                return HttpResponse(data)
            data = json.dumps({'verification_username_result': 'false'})
            return HttpResponse(data)
        return render(request, 'forget_passwd.html')
    if request.method == "POST":
        # 假如POST请求
        username = request.POST.get('username')
        old_pwd = request.POST.get('password')
        # 判断特殊情况下用户名和密码没有填写, 否则返回提示信息
        if username and old_pwd:
            # 新密码加盐
            new_pwd, salt = get_hashlib_salt(old_pwd)
            tel = request.POST.get('tel')
            if models.RegisterFirst.objects.filter(username=username, tel=tel):
                try:
                    with transaction.atomic():
                        models.HashlibSalt.objects.filter(registerfirst__username=username).update(salt=salt)
                        models.RegisterFirst.objects.filter(username=username).update(password=new_pwd)
                    return HttpResponse("<script>alert('更换密码成功, 请使用新密码登录');location.href='/';</script>")
                except Exception:
                    return HttpResponse("<script>alert('更改密码失败');</script>")
            else:
                return HttpResponse("<script>alert('账号与手机号不符合');</script>")
        return HttpResponse("<script>alert('信息填写不完整');</script>")


@csrf_exempt
def sms_verification(request):
    if request.POST.get('code', None):
        code = request.POST.get('code', None)
        if code != request.session.get('code_vfi'):
            return HttpResponse('false')
        return HttpResponse('true')
    request.session['code_vfi'] = '123456'
    return HttpResponse('发送成功')
    # if code_verification(request):
    #     return HttpResponse('发送成功')
    # return HttpResponse('发送失败')

#
# def leave(request):
#     if request.method == 'GET':
#         return render(request, 'leave.html')


@csrf_exempt
def update_user_photo(request):
    data = request.FILES.get('file')
    username = request.session.get('username')
    try:
        models.RegisterFirst.objects.filter(username=username).update(user_photo=data.file.read())
    except Exception:
        pass
    else:
        write_session(request, username=username)
    return HttpResponse({'isSuccess': 'ok'})


"""
    注册，登陆逻辑：
    注册：
        1：经过第一步注册后，将注册信息输入数据库，选择专业关联第一步，专业选择完成，填写后续信息，关联专业
            first 《==  two  《== three
"""


# 登录界面
def login(request):
    if request.method == 'GET':
        return is_register(request)
    elif request.method == 'POST':
        if request.POST.get('login_radio') == '1':
            # 如果用户选择不保存密码,退出浏览器则session失效
            request.session.set_expiry(0)
        # 如果需要在页面展示的信息,在此处添加到session
        return is_register(request)


class Register(object):
    def __init__(self):
        pass

    @staticmethod
    def register_one(request):
        if request.method == 'GET':
            # 判断用户是否已经注册，否则跳转首页
            username = request.session.get('username', None)
            if not username:
                # 用户未登陆
                register_one = myforms.RegisterOne()
                return render(request, 'register_one.html', locals())
            return HttpResponse("<script>alert('如需注册新用户，请先退出当前登陆状态');location.href='/';</script>")
        else:
            register_one = myforms.RegisterOne(request.POST)
            reg_p= request.POST.get('result_result', None)
            if register_one.is_valid():
                data = register_one.cleaned_data
                data.pop('repeat_password')
                if reg_p == '老师注册':
                    number = get_tc_card_id()
                else:
                    number = get_card_id()
                register_date = datetime.datetime.now().date()
                # 密码加密, 加固定盐， 也可以更改为加随机盐
                data['password'], salt = get_hashlib_salt(data['password'])
                try:
                    with transaction.atomic():
                        salt_obj = models.HashlibSalt.objects.create(salt=salt)
                        one = models.RegisterFirst.objects.create(user_salt=salt_obj,
                                                                  number=number, register_date=register_date,
                                                                  register_one_status=1, **data)
                        if reg_p == '老师注册':
                            gid = models.Group.objects.filter(groupName='意向教师').first()
                            models.UserGroup.objects.create(user_id=one.id, group_id=gid.id)
                            return HttpResponse("<script>alert('请牢记您的账号信息,等待管理员开通权限');</script>")
                        gid = models.Group.objects.filter(groupName='意向学生').first()
                        models.UserGroup.objects.create(user_id=one.id, group_id=gid.id)
                        # 如果注册信息写入数据库成功，则添加需要在页面展示的信息到session
                        write_session(request, one.username)
                        return HttpResponseRedirect('/register_two/')
                except Exception as e:
                    print(e)
                    request.session.clear()
                    return HttpResponse("<script>alert('遇到错误，请重新尝试或联系管理员');location.href='/';</script>")
            # register_one = myforms.RegisterOne(request.POST)
            return render(request, 'register_one.html', locals())

    @staticmethod
    def register_two(request):
        if request.method == 'GET':
            # 判断用户是否已经进行选择，防止用户直接通过路径进行操作
            username = request.session.get('username', None)
            if not username:
                return HttpResponse("<script>alert('请先进行登陆！');"
                                    "location.href='/';</script>")
            try:
                models.RegisterTwo.objects.filter(
                    first__username=username).values_list('register_two_status').first()[0]
            except Exception:
                major = models.Major.objects.all()
                major_dict = {}
                for i in major:
                    major_dict[(i.caption, i.image)] = list(models.MajorChild.objects.filter(
                        major_id=i.id).values_list('id', 'caption'))
                major_main_select = list(models.RegisterTwo.objects.filter(
                    first__username=username).values_list('major_child_id', 'major_child__caption'))
                return render(request, 'register_two.html', locals())
            else:
                return HttpResponse(
                    "<script>alert('信息已经保存，如需更改请登陆后在首页更新！');location.href='/';</script>")

        elif request.method == 'POST':
            username = request.session.get('username', None)
            if not username:
                return HttpResponse("<script>alert('请先进行登陆！');"
                                    "location.href='/';</script>")

            if request.POST.get('p', None):
                obj = list(models.RegisterTwo.objects.filter(
                    first__username=username).values_list('major_child'))
                if len(obj) >= 10:
                    return HttpResponse('error')
                a = request.POST.get('p').split(',')
                try:
                    two = models.RegisterTwo.objects.create(
                        major_child_id=a[0],
                        first_id=models.RegisterFirst.objects.filter(
                            username=username).values_list('id').first()[0],
                        register_two_status=1
                    )
                except Exception as e:
                    print(e)
                    return HttpResponse('update_error')
                else:
                    return HttpResponse(json.dumps(a))
            elif request.POST.get('delete', None):
                did = request.POST.get('delete', None)
                try:
                    obj = models.RegisterTwo.objects.filter(major_child_id=did).delete()
                except Exception as e:
                    print(e)
                    return HttpResponse('false')
                else:
                    return HttpResponse('ok')
        return render(request, 'register_two.html', locals())

    @staticmethod
    def register_three(request):
        if request.method == 'GET':
            username = request.session.get('username', None)
            if not username:
                return HttpResponse("<script>alert('请先进行登陆！');"
                                    "location.href='/';</script>")
            try:
                models.RegisterThree.objects.filter(
                    first__username=username).values_list('register_three_status').first()[0]
            except Exception:
                major_main_select = list(models.RegisterTwo.objects.filter(
                    first__username=username).values_list('id', 'major_child__caption'))
                register_three = myforms.RegisterThree()
                return render(request, 'register_three.html', locals())
            else:
                return HttpResponse("<script>alert('信息已经保存，如需更改请登陆后在首页更新！');"
                                    "location.href='/';</script>")

        elif request.method == 'POST':
            username = request.session.get('username', None)
            if not username:
                return HttpResponse("<script>alert('Sorry，身份验证失败，请重新登陆！');"
                                    "location.href='/';</script>")
            register_two_id = request.POST.get('major_main_select', None)
            models.RegisterTwo.objects.filter(first__username=username).update(status=False)
            models.RegisterTwo.objects.filter(id=register_two_id).update(status=True)
            register_three = myforms.RegisterThree(request.POST)

            if register_three.is_valid():
                data = register_three.cleaned_data
                models.RegisterThree.objects.create(**data,
                                                    first_id=models.RegisterFirst.objects.filter(
                                                        username=username).values_list('id').first()[0],
                                                    register_three_status=1)
                return HttpResponseRedirect('/register_four/')
            else:
                major_main_select = list(models.RegisterTwo.objects.filter(
                    first__username=username).values_list('id', 'major_child__caption'))
                register_three = myforms.RegisterThree(request.POST)
                return render(request, 'register_three.html', locals())

    @staticmethod
    def register_four(request):
        if request.method == 'GET':
            year = datetime.datetime.now().year
            return render(request, 'register_four.html', locals())


# 查询自己的信息
# def select_me(request):
#     if request.method == 'GET':
#         models.Student.objects.filter(name=request.session.get('username'))
#         return render(request, 'select_me.html')


# 管理页面首页
@is_login
@locked
def student_menu(request):
    username = request.session.get('username', None)
    if username:
        # permission_list, permission_dict = get_permission(username, request)
        # html = get_permission_html(permission_dict)
        return render(request, "student_menu.html", locals())
    else:
        return HttpResponseRedirect('/')


# 注销登陆
def logout(request):
    request.session.clear()
    return HttpResponseRedirect('/')


def manage_add(request):
    """
    测试意外删库时执行，生成默认数据
    :param request:
    :return:
    """
    with transaction.atomic():
        cls = GetManage()
        # cls.make_user()
        cls.make_group()
        # cls.make_user_group()
        cls.make_table()
        cls.make_table_permission()
        cls.make_permission()
        cls.make_group_permission()
        cls.make_major()
        cls.make_sex()
        cls.make_type()
        cls.make_status()
        cls.make_no_permission()
    return HttpResponse('success full')


def upload_image(request):
    if request.method == "GET":
        # file = os.path.join(os.getcwd(), 'statics', 'USER_DEFAULT_PHOTO.png')
        # with open(file, 'rb') as f1:
        #     DEFAULT_PHOTO = f1.read()
        # print(DEFAULT_PHOTO)
        # f = BytesIO()
        # f.write(DEFAULT_PHOTO)
        # InMemoryUploadedFile 需要的参数：
        # file, field_name, name, content_type, size, charset, content_type_extra = None
        # image = InMemoryUploadedFile(f, None, '用户头像', None, len(DEFAULT_PHOTO), None, None)
        # img = models.RegisterFirst.objects.filter(username='huyu123456').values('user_photo')
        # print(img)
        # img = models.RegisterFirst.objects.filter(
        #     username='yuanxiong123').first().user_photo
        # # print(img)
        # # f = BytesIO(img)
        # # image = InMemoryUploadedFile(f, None, '用户头像', None, len(img), None, None)
        # img = base64.b64encode(img).decode()
        img = get_user_photo('yuanxiong123')
        return render(request, 'upload_image.html', locals())
    else:
        # img = request.FILES.get('img')
        # models.ImageTest.objects.create(img=img.file.read())
        # with open('/Users/yuanxiong/PycharmProjects/学校管理项目/Main/金三胖.jpg', mode='wb') as f:
        #     f.write(img.file.read())
        # img = models.ImageTest.objects.filter().first().img
        # img = base64.b64encode(img).decode()
        return render(request, 'upload_image.html', locals())


# # ---------------------------------    学生个人信息展示   --------------------------------------
#
# def school_manage_test(request):
#     obj = list(User.objects.filter(card_id='ST-1904105920').values_list(
#         'username__class_info__class_name',
#         'username__class_info__grade_name__grade_name'
#     ))
#
#     print(type(obj[0]))
#     return HttpResponse(obj[0])
#
#
# # ---------------------------------    学生信息页面   --------------------------------------
#
# # @is_login
# # def add_student(request):
# #     if request.method == 'GET':
# #         obj = forms.Student()
# #         return render(request, 'add_student.html', locals())
#
#
# @is_login
# def school_manage_many_add_student(request):
#     if request.method == 'GET':
#         return render(request, 'school_manage_many_add_student.html', locals())
#     elif request.method == 'POST':
#         file = request.FILES.get('files')
#         with open(os.getcwd() + '/SchoolManage/recv_files/' + file.name, 'wb') as f:
#             f.write(file.read())
#             f.flush()
#         workbook = xlrd.open_workbook(os.getcwd() + '/SchoolManage/recv_files/' + file.name)
#         sheet = workbook.sheet_by_name('sheet1')
#         for i in range(1, sheet.nrows):
#             lst = sheet.row_values(i, 0)
#             stu = Student.objects.create(
#                 real_name=lst[0],
#                 age=lst[1],
#                 tel=lst[2],
#                 register_date=lst[3],
#                 id_card=lst[4],
#                 location_of_household_registration=lst[5],
#                 tel_two=lst[6],
#                 address=lst[7],
#                 market=lst[8],
#                 class_info_id=int(lst[9]),
#                 sex_id=int(lst[10]),
#                 type_id=int(lst[11]),
#                 major_id=int(lst[12]),
#                 status_id=int(lst[13])
#             )
#             User.objects.create(
#                 username=stu,
#                 card_id=card_id(),
#                 password='123'
#             )
#         os.remove(os.getcwd() + '/SchoolManage/recv_files/' + file.name)
#         return HttpResponseRedirect('/index/', locals())
#
#
# @is_login
# def school_manage_add_student(request):
#     print(request.session.get('username'))
#     if request.method == 'GET':
#         class_names = Classes.objects.all()
#         sex = Sex.objects.all()
#         type = StudentType.objects.all()
#         major = StudentMajor.objects.all()
#         status = StudentStatus.objects.all()
#         return render(request, 'school_manage_add_student.html', locals())
#     elif request.method == 'POST':
#         sbm = request.POST.get('sbm')
#         d = do_request(request.POST,
#                        ('class_info', 'type', 'major', 'status', 'sex'),
#                        ('sbm', 'csrfmiddlewaretoken'))
#         print(d)
#         stu = Student.objects.create(**d)
#         User.objects.create(
#             username=stu,
#             card_id=card_id(),
#             password='123'
#         )
#         if sbm == '下一个':
#             return HttpResponseRedirect('/add_student/', locals())
#         elif sbm == '提交保存':
#             return HttpResponseRedirect('/index/', locals())
#
#
# @is_login
# def school_manage_display_student(request):
#     obj = Student.objects.all()  # 获取所有student信息
#     return render(request, 'school_manage_display_student.html', locals())
#
#
# @is_login
# def school_manage_delete_student(request):
#     if request.method == 'GET':
#         cid = request.GET.get("cid")
#         Student.objects.filter(id__exact=cid).delete()
#         return HttpResponseRedirect('/display_student/', locals())
#
#
# @is_login
# def school_manage_update_student(request):
#     if request.method == 'GET':
#         class_names = Classes.objects.all()
#         sex = Sex.objects.all()
#         type = StudentType.objects.all()
#         major = StudentMajor.objects.all()
#         status = StudentStatus.objects.all()
#         cid = request.GET.get('cid')
#         obj = Student.objects.filter(id__exact=cid)[0]
#         return render(request, 'school_manage_update_student.html', locals())
#     elif request.method == 'POST':
#         if request.POST.get('sbm') == '保存提交':
#             cid = request.GET.get('cid')
#             d = do_request(request.POST,
#                            ('class_info', 'type', 'major', 'status', 'sex'),
#                            ('sbm', 'csrfmiddlewaretoken'))
#             Student.objects.filter(id=cid).update(**d)
#         return HttpResponseRedirect('/display_student/', locals())
#
#
# # --------------------------------------- 转换储存 -------------------------------------------
#
#
# def do_request(request, args, args1):
#     '''
#         :return:
#         把request信息转成可建表的字典
#         :param request: request(POST) query结合
#         :param args: 元祖,包含所有的外键
#         :param args1: 多余的键
#         :return: 建表字典
#     '''
#     d = dict(request)
#     for i in args1:
#         d.pop(i)
#     for k, v in d.items():
#         d[k] = v[0]
#     for foreign in args:
#         d[foreign + '_id'] = int(d[foreign])
#         d.pop(foreign)
#     return d
#
#

#
