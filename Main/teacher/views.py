from django.shortcuts import render, HttpResponse, redirect, reverse, render_to_response
from functools import wraps
from ..models import *
from ..get_result import is_login
import time
import os
# Create your views here.
import json


class Work(object):
    def __init__(self):
        self.id = ''
        # 部门用来表示是哪个部门的工作,
        self.department = ''
        # 表示给这个部门的某个教师分配的工作
        self.tea_id = ''
        # 工作标题
        self.title = ''
        # 工作内容
        self.content = ''
        # 工作类型(日/周/月)
        self.work_type = ''
        # 工作状态,
        self.work_state = ""
        # 工作任务生成时间
        self.date = ''
        # 工作完成时间
        self.finish = ''


# def check_login(func):
#     @wraps(func)
#     def inner(request, *args, **kwargs):
#         next_path = request.get_full_path()
#         print(next_path)
#         print()
#         if request.session.get('is_login') == '1':
#             return func(request, *args, **kwargs)
#         else:
#             return redirect('/index/login.html')
#     return inner


def locked(func):
    @wraps(func)
    def inner(request, *args, **kwargs):

        if 'active' in request.session:
            if request.session['active'] == '1':
                return func(request, *args, **kwargs)
            else:
                return redirect('/teacher_manage/locked.html')
        else:
            return func(request, *args, **kwargs)

    return inner


@is_login
@locked
def index(request):
    user_id = request.session.get('user_id')
    user = RegisterFirst.objects.filter(id=user_id)
    if user:
        tea = user[0]
        return render(request, 'lg/index.html', locals())
    return render(request, 'lg/index.html', locals())
    # return render(request, 'login.html')

@is_login
@locked
def table_static(request):
    try:
        id = request.session.get('user_id')
        tea = RegisterFirst.objects.filter(id=id)[0]
    except IndexError:
        return render(request, 'login.html')
    except:
        return render(request, 'lg/error-404.html')
    work = Work_arrange.objects.filter(id=id)
    work_day = work.filter(work_type=1)
    unfinsh_work_day = work_day.filter(work_state=1)
    finsh_work_day = work_day.filter(work_state=3)
    working_day = work_day.filter(work_state=6)
    help_work_day = work_day.filter(work_state=4)

    return render(request, 'lg/table-static.html', locals())


@is_login
@locked
def table_responsive(request):
    try:
        id = request.session.get('user_id')
        tea = RegisterFirst.objects.filter(id=id)[0]
    except IndexError:
        return render(request, 'login.html')
    except:
        return render(request, 'lg/error-404.html')
    work = Work_arrange.objects.filter(id=id)
    work_day = work.filter(work_type=2)
    unfinsh_work_day = work_day.filter(work_state=1)
    finsh_work_day = work_day.filter(work_state=3)
    working_day = work_day.filter(work_state=6)
    help_work_day = work_day.filter(work_state=4)

    return render(request, 'lg/table-responsive.html', locals())


@is_login
@locked
def table_datatable(request):
    try:
        id = request.session.get('user_id')
        tea = RegisterFirst.objects.filter(id=id)[0]
    except IndexError:
        return render(request, 'login.html')
    except:
        return render(request, 'lg/error-404.html')

    work = Work_arrange.objects.filter(id=id)
    work_day = work.filter(work_type=3)
    unfinsh_work_day = work_day.filter(work_state=1)
    finsh_work_day = work_day.filter(work_state=3)
    working_day = work_day.filter(work_state=6)
    help_work_day = work_day.filter(work_state=4)
    return render(request, 'lg/table-datatable.html', locals())


def login_views(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        teas = RegisterFirst.objects.filter(username=username, password=password)
        if teas:
            tea = teas[0]
            request.session['is_login'] = '1'
            request.session['user_id'] = tea.id
            request.session.set_expiry(0)
            response = redirect('index.html')
            if 'rempwd' in request.POST:
                response.set_cookie('username', username)
                response.set_cookie('password', password)
                return response
            return response
        else:
            msg = "账户或密码错误"
            return render(request, 'login.html', {'msg': msg})


@is_login
@locked
def message_view(request):
    id = request.session.get('user_id')
    teas = RegisterFirst.objects.filter(id=id)
    if teas:
        tea = teas[0]
        work = Work_arrange.objects.filter(id=id)[0]
        return render(request, 'lg/message-view.html', locals())
    else:
        return render(request, 'lg/error-404.html')


@is_login
@locked
def inbox_view(request):
    id = request.session.get('user_id')
    tea = RegisterFirst.objects.filter(id=id).first()
    if "send" in request.GET:
        send_inform = Inform.objects.filter(send_from_tea=id)
        lists = []
        for inform in send_inform:
            json_list = {
                'send_to_dpt': list(DepToTea.objects.filter(teacher_id=inform.send_to_tea).values_list(
                    'department__caption').first())[0],
                'send_from_dpt': list(DepToTea.objects.filter(teacher_id=inform.send_from_tea).values_list(
                    'department__caption').first())[0],
                'send_to_tea': inform.send_to_tea.username,
                'send_from_tea': inform.send_from_tea.username, 'title': inform.title,
                'times': str(inform.times)}
            lists.append(json_list)
        send = json.dumps(lists, ensure_ascii=False)
        return HttpResponse(json.dumps(lists, ensure_ascii=False), content_type="application/json,charset=utf-8")

    elif 'form' in request.GET:
        from_inform = Inform.objects.filter(send_to_tea=tea.id)
        lists = []
        for inform in from_inform:
            json_list = {
                'send_to_dpt': list(DepToTea.objects.filter(teacher_id=inform.send_to_tea).values_list(
                    'department__caption').first())[0],
                'send_from_dpt': list(DepToTea.objects.filter(teacher_id=inform.send_from_tea).values_list(
                    'department__caption').first())[0],
                'send_to_tea': inform.send_to_tea.username,
                'send_from_tea': inform.send_from_tea.username, 'title': inform.title,
                'times': str(inform.times)}
            lists.append(json_list)

        return HttpResponse(json.dumps(lists, ensure_ascii=False), content_type="application/json,charset=utf-8")

    elif 'all' in request.GET:
        send_inform = Inform.objects.filter(send_from_tea=id)
        from_inform = Inform.objects.filter(send_to_tea=tea.id)

        lists = []
        for inform in from_inform:
            json_list = {
                'send_to_dpt': list(
                    DepToTea.objects.filter(teacher_id=inform.send_to_tea).values_list(
                        'department__caption').first())[0],
                'send_from_dpt': list(DepToTea.objects.filter(teacher_id=inform.send_from_tea).values_list(
                    'department__caption').first())[0],
                'send_to_tea': inform.send_to_tea.username,
                'send_from_tea': inform.send_from_tea.username, 'title': inform.title,
                'times': str(inform.times)}
            lists.append(json_list)
        for inform in send_inform:
            json_list = {
                'send_to_dpt': list(
                    DepToTea.objects.filter(teacher_id=inform.send_to_tea).values_list(
                        'department__caption').first())[0],
                'send_from_dpt': list(DepToTea.objects.filter(teacher_id=inform.send_from_tea).values_list(
                    'department__caption').first())[0],
                'send_to_tea': inform.send_to_tea.username,
                'send_from_tea': inform.send_from_tea.username, 'title': inform.title,
                'times': str(inform.times)}
            lists.append(json_list)
        return HttpResponse(json.dumps(lists, ensure_ascii=False), content_type="application/json,charset=utf-8")
    elif 'dustbin' in request.GET:
        send_inform = Inform.objects.filter(send_from_tea=id, isActive=False)
        from_inform = Inform.objects.filter(send_to_tea=tea.id, isActive=False)

        lists = []
        for inform in from_inform:
            json_list = {
                'send_to_dpt': list(
                    DepToTea.objects.filter(teacher_id=inform.send_to_tea).values_list(
                        'department__caption').first())[0],
                'send_from_dpt': list(DepToTea.objects.filter(teacher_id=inform.send_from_tea).values_list(
                    'department__caption').first())[0],
                'send_to_tea': inform.send_to_tea.username,
                'send_from_tea': inform.send_from_tea.username, 'title': inform.title,
                'times': str(inform.times)}
            lists.append(json_list)
        for inform in send_inform:
            json_list = {
                'send_to_dpt': list(
                    DepToTea.objects.filter(teacher_id=inform.send_to_tea).values_list(
                        'department__caption').first())[0],
                'send_from_dpt': list(DepToTea.objects.filter(teacher_id=inform.send_from_tea).values_list(
                    'department__caption').first())[0],
                'send_to_tea': inform.send_to_tea.username,
                'send_from_tea': inform.send_from_tea.username, 'title': inform.title,
                'times': str(inform.times)}
            lists.append(json_list)
        return HttpResponse(json.dumps(lists, ensure_ascii=False), content_type="application/json,charset=utf-8")

    else:
        return render(request, 'lg/inbox.html', locals())


@is_login
@locked
def compose_view(request):
    id = request.session.get('user_id')   # 获取用户id
    tea = RegisterFirst.objects.filter(id=id).first()   # 获取用户对象
    if request.method == 'GET':
        id = request.session.get('user_id')
        if 'dep' in request.GET:
            department = Major.objects.all()
            json_list = []
            for dep in department:
                json_dict = {
                    'id': dep.id,
                    'dep_name': dep.caption
                }
                json_list.append(json_dict)
            dep_all = json.dumps(json_list, ensure_ascii=False)

            return HttpResponse(json.dumps(json_list, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
        elif 'pid' in request.GET:
            pid = request.GET.get('pid')
            teachers = list(DepToTea.objects.filter(department_id=pid).values('id', 'teacher__username', 'teacher__id'))
            json_list = []
            for teacher in teachers:
                if teacher['teacher__id'] == id:
                    continue
                json_dict = {
                    'user_id': teacher['id'],
                    'user_name': teacher['teacher__username'],

                }
                json_list.append(json_dict)
            return HttpResponse(json.dumps(json_list, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
        return render(request, 'lg/compose.html', locals())

    else:
        inf = Inform()
        if 'file' in request.FILES:
            file = request.FILES.get('file')
            t = time.time()
            file_name = '%.0f' % t + '.' + file.name.split('.')[-1]
            print(os.getcwd())
            path = 'Main/teacher/file/' + file_name
            f = open(path, 'wb')
            for tun in file:
                f.write(tun)
            f.close()
            inf.filed_name = file.name
            inf.local_file = file_name
        else:
            inf.filed_name = '...'
            inf.local_file = '...'

        tid = list(DepToTea.objects.filter(id=request.POST.get('to_tea', None)).values_list('teacher_id').first())[0]

        # 哪个老师发送
        inf.send_from_tea = RegisterFirst.objects.filter(username=request.session.get('username', None)).first()
        # 发送给哪个老师
        inf.send_to_tea = RegisterFirst.objects.filter(id=tid).first()
        # 标题
        inf.title = request.POST.get('title')
        inf.content = request.POST.get('content')
        inf.times = time.time()
        inf.save()

        return HttpResponse("<script>alert('发送成功');location.href='';</script>")


@is_login
@locked
def logout(request):
    request.session.flush()
    return redirect('/lg/index/login.html')


@is_login
@locked
def dashboard2(request):
    return render(request, 'lg/dashboard2.html')


def test(request):
    pid = 12
    teachers = list(DepToTea.objects.filter(department_id=12).values('id', 'teacher__username', 'teacher__id'))
    print(teachers)
    return HttpResponse('ok')

@is_login
@locked
def my_course(request):
    tea_id = request.session['user_id']
    tea = RegisterFirst.objects.filter(id=tea_id).first()
    course = Course.objects.filter(grade__teacher=tea).all()
    return render(request, 'lg/ui-buttons.html', locals())


@is_login
@locked
def validation(request):
    userid = request.session['user_id']
    tea = RegisterFirst.objects.filter(id=userid)[0]
    id = request.GET.get('id')
    # print(id)
    teachers = RegisterFirst.objects.filter(deptotea__id=id).first()
    # print(teachers)
    # teachers = list(DepToTea.objects.filter(department__id=id).values('id', 'teacher__username', 'teacher__id'))
    # print(teachers)
    # teachers = RegisterFirst.objects.filter(id=id)
    # if teachers:
    #     teacher = teachers[0]
    return render(request, 'lg/form-validation.html', locals())


@is_login
@locked
def xeditable(request):
    id = request.session['user_id']
    tea = RegisterFirst.objects.filter(id=id)[0]
    peple = DepToTea.objects.all()
    # tea = Teacher.objects.filter(user_id=1)
    return render(request, 'lg/form-xeditable.html', locals())


@is_login
@locked
def calendar(request):
    return render(request, 'lg/calendar.html')


@is_login
@locked
def flot_chart(request):
    return render(request, 'lg/flot-chart.html')


@is_login
@locked
def check_day(request):
    return render(request, 'lg/check_day.html')


# @check_login
@locked
def check_week(request):
    return render(request, 'lg/timeline.html')


@is_login
@locked
def inform_filed(request):
    return render(request, 'lg/inform-filed.html')


@locked# @check_login
@locked
def forgot_password(request):
    return render(request, 'lg/forgot-password.html')


@is_login
@locked
def user_info(request):
    if request.method == 'GET':
        return render(request, 'lg/user_info.html')
    else:
        return render(request, 'lg/user_info.html')


@is_login
@locked
def course_info(request):
    return render(request, 'lg/course_info.html')


#
# @check_login
# @locked
# def test(request):
#     return render(request, 'lg/test.html')

@is_login
@locked
def del_cookie(request):
    response = HttpResponse('quit')
    try:
        response.delete_cookie('username')
        request.session.flush()
    except Exception as e:
        return render(request, 'lg/error-500.html', {'error': e})
    return response


@is_login
@locked
def settings(request):
    return render(request, 'lg/settings.html')


@is_login
@locked
def registration(request):
    return render(request, 'lg/registration.html')


@is_login
@locked
def reset_pwd(request):
    return render(request, 'lg/reset-password.html')


@is_login
@locked
def unlock(request):
    if request.method == 'GET':
        return render(request, 'lg/unlocked.html')
    else:
        pwd = request.POST.get('unpwd')
        request.session['unlock'] = pwd
        request.session['active'] = '0'
        return redirect('/teacher_manage/locked.html')


# @check_login
def lockeds(request):
    if request.method == 'GET':
        return render(request, 'lg/locked.html')
    else:
        pwd = request.POST.get('unpwd')
        if pwd == request.session['unlock']:
            request.session['active'] = '1'
            number = list(RegisterFirst.objects.filter(username=request.session.get(
                'username', None)).values_list('number').first())[0]
            if 'ST' in number:
                return redirect('/student_menu/')
            g_list = list(RegisterFirst.objects.filter(username=request.session.get(
                'username', None)).values_list('usergroup__group__groupName').first())
            if '管理员' in g_list:
                return redirect('/back_manage/')
            return redirect('/teacher_manage/')
        else:
            msg = "解锁失败, 请输入正确密码!"
            return render(request, 'lg/locked.html', locals())
