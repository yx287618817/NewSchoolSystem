from django.shortcuts import render, HttpResponse, redirect, reverse, render_to_response
from functools import wraps
from ..models import *
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
                return redirect('/lg/index/locked.html')
        else:
            return func(request, *args, **kwargs)

    return inner


# @check_login
@locked
def index(request):
    print("主页路由")
    user_id = request.session.get('user_id')
    print(user_id)
    user = RegisterFirst.objects.filter(id=user_id)
    if user:
        print('主页')
        tea = user[0]
        return render(request, 'lg/index.html', locals())
    return render(request, 'lg/index.html', locals())
    # return render(request, 'lg/login.html')


# @check_login
@locked
def table_static(request):
    try:
        id = request.session.get('user_id')
        tea = RegisterFirst.objects.filter(id=id)[0]
    except IndexError:
        return render(request, 'lg/login.html')
    except:
        return render(request, 'lg/error-404.html')
    work = Work_arrange.objects.filter(id=id)
    work_day = work.filter(work_type=1)
    unfinsh_work_day = work_day.filter(work_state=1)
    finsh_work_day = work_day.filter(work_state=3)
    working_day = work_day.filter(work_state=6)
    help_work_day = work_day.filter(work_state=4)

    return render(request, 'lg/table-static.html', locals())


# @check_login
@locked
def table_responsive(request):
    try:
        id = request.session.get('user_id')
        tea = RegisterFirst.objects.filter(id=id)[0]
        print('respnsive', id)
    except IndexError:
        return render(request, 'lg/login.html')
    except:
        return render(request, 'lg/error-404.html')
    work = Work_arrange.objects.filter(id=id)
    work_day = work.filter(work_type=2)
    unfinsh_work_day = work_day.filter(work_state=1)
    finsh_work_day = work_day.filter(work_state=3)
    working_day = work_day.filter(work_state=6)
    help_work_day = work_day.filter(work_state=4)

    return render(request, 'lg/table-responsive.html', locals())


# @check_login
@locked
def table_datatable(request):
    try:
        id = request.session.get('user_id')
        tea = RegisterFirst.objects.filter(id=id)[0]
        print('database', id)
    except IndexError:
        return render(request, 'lg/login.html')
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
        return render(request, 'lg/login.html')
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
            return render(request, 'lg/login.html', {'msg': msg})


# @check_login
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


# @check_login
@locked
def inbox_view(request):
    id = request.session.get('user_id')
    teas = RegisterFirst.objects.filter(id=id)
    tea = teas[0]
    if "send" in request.GET:
        send_inform = Inform.objects.filter(send_from_tea=id)
        lists = []
        for inform in send_inform:
            json_list = {'send_to_dpt': inform.send_to_dpt.dep_name, 'send_to_tea': inform.send_to_tea.username,
                         'send_from_dpt': inform.send_from_dpt.dep_name,
                         'send_from_tea': inform.send_from_tea.username, 'title': inform.title,
                         'times': str(inform.times)}
            lists.append(json_list)
        send = json.dumps(lists, ensure_ascii=False)
        return HttpResponse(json.dumps(lists, ensure_ascii=False), content_type="application/json,charset=utf-8")

    elif 'form' in request.GET:
        from_inform = Inform.objects.filter(send_to_tea=teas[0].id)
        lists = []
        for inform in from_inform:
            json_list = {'send_to_dpt': inform.send_to_dpt.dep_name, 'send_to_tea': inform.send_to_tea.username,
                         'send_from_dpt': inform.send_from_dpt.dep_name,
                         'send_from_tea': inform.send_from_tea.username, 'title': inform.title,
                         'times': str(inform.times)}
            lists.append(json_list)

        return HttpResponse(json.dumps(lists, ensure_ascii=False), content_type="application/json,charset=utf-8")

    elif 'all' in request.GET:
        send_inform = Inform.objects.filter(send_from_tea=id)
        from_inform = Inform.objects.filter(send_to_tea=teas[0].id)

        lists = []
        for inform in from_inform:
            json_list = {'send_to_dpt': inform.send_to_dpt.dep_name, 'send_to_tea': inform.send_to_tea.username,
                         'send_from_dpt': inform.send_from_dpt.dep_name,
                         'send_from_tea': inform.send_from_tea.username, 'title': inform.title,
                         'times': str(inform.times)}
            lists.append(json_list)
        for inform in send_inform:
            json_list = {'send_to_dpt': inform.send_to_dpt.dep_name, 'send_to_tea': inform.send_to_tea.username,
                         'send_from_dpt': inform.send_from_dpt.dep_name,
                         'send_from_tea': inform.send_from_tea.username, 'title': inform.title,
                         'times': str(inform.times)}
            lists.append(json_list)
        print(lists)
        return HttpResponse(json.dumps(lists, ensure_ascii=False), content_type="application/json,charset=utf-8")
    elif 'dustbin' in request.GET:
        send_inform = Inform.objects.filter(send_from_tea=id, isActive=False)
        from_inform = Inform.objects.filter(send_to_tea=teas[0].id, isActive=False)

        lists = []
        for inform in from_inform:
            json_list = {'send_to_dpt': inform.send_to_dpt.dep_name, 'send_to_tea': inform.send_to_tea.username,
                         'send_from_dpt': inform.send_from_dpt.dep_name,
                         'send_from_tea': inform.send_from_tea.username, 'title': inform.title,
                         'times': str(inform.times)}
            lists.append(json_list)
        for inform in send_inform:
            json_list = {'send_to_dpt': inform.send_to_dpt.dep_name, 'send_to_tea': inform.send_to_tea.username,
                         'send_from_dpt': inform.send_from_dpt.dep_name,
                         'send_from_tea': inform.send_from_tea.username, 'title': inform.title,
                         'times': str(inform.times)}
            lists.append(json_list)
        return HttpResponse(json.dumps(lists, ensure_ascii=False), content_type="application/json,charset=utf-8")

    else:
        return render(request, 'lg/inbox.html', locals())


# @check_login
@locked
def compose_view(request):
    id = request.session.get('user_id')
    tea = RegisterFirst.objects.filter(id=id)[0]

    print('id', id)
    teas = RegisterFirst.objects.filter(id=id)
    print(teas)
    if request.method == 'GET':
        id = request.session.get('user_id')
        teas = RegisterFirst.objects.filter(id=id)
        tea = teas[0]
        if 'dep' in request.GET:
            id = request.session.get('user_id')
            teas = RegisterFirst.objects.filter(id=id)[0]
            department = Major.objects.all()
            # print(department[0].dep_name)
            json_list = []
            for dep in department:
                print(dep.id)
                json_dict = {
                    'id': dep.id,
                    'dep_name': dep.caption
                }
                json_list.append(json_dict)
            print(json_list)
            dep_all = json.dumps(json_list, ensure_ascii=False)

            return HttpResponse(json.dumps(json_list, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
        elif 'pid' in request.GET:
            pid = request.GET.get('pid')
            teachers = list(DepToTea.objects.filter(department__id=pid).values('id', 'teacher__username', 'teacher__id'))
            print(teachers)
            json_list = []
            for teacher in teachers:
                print(teacher['id'])

                if teacher['teacher__id'] == id:
                    continue
                json_dict = {
                    'user_id': teacher['id'],
                    'user_name': teacher['teacher__username'],

                }
                json_list.append(json_dict)
            print(json_list)
            return HttpResponse(json.dumps(json_list, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
        return render(request, 'lg/compose.html', locals())

    else:
        # 接收对应部门
        to_dpt = request.POST.get('to_dpt')
        # print(to_dpt)
        # 接收对应老师
        to_tea = request.POST.get('to_tea')
        # print(to_tea)
        # 标题
        title = request.POST.get('title')
        # print(title)
        # 内容
        content = request.POST.get('content')
        # print(content)
        # 文件

        # 需要保存的字段有:send_to_dpt, send_to_tea, send_from_dpt, send_from_tea, title,
        # content, file_name, file,

        if 'file' in request.FILES:
            file = request.FILES.get('file')
            t = time.time()
            file_name = '%.0f' % t + '.' + file.name.split('.')[-1]
            print(file_name)

            tea = teas[0]
            send_from_dpt = DepToTea.objects.filter(teacher__id=id)[0].department
            # print(send_from_dpt.id)
            send_from_tea = tea.id
            # print(os.path.abspath(__file__))
            path = 'Main/teacher/file/' + file_name
            f = open(path, 'wb')
            for tun in file:
                f.write(tun)
            f.close()
            inf = Inform()
            inf.send_to_dpt_id = to_dpt
            inf.send_to_tea_id = to_tea
            inf.send_from_dpt_id = DepToTea.objects.filter(teacher__id=id)[0].department.id
            inf.send_from_tea_id = id
            inf.title = title
            inf.content = content
            inf.filed_name = file.name
            inf.local_file = file_name
            inf.save()
        else:
            tea = teas[0]
            inf = Inform()
            inf.send_to_dpt_id = to_dpt
            inf.send_to_tea_id = to_tea
            inf.send_from_dpt_id = tea.department_id
            inf.send_from_tea_id = id
            inf.title = title
            inf.content = content
            inf.save()
        return HttpResponse("发送成功")


# @check_login
@locked
def logout(request):
    request.session.flush()
    return redirect('/lg/index/login.html')


# @check_login
@locked
def dashboard2(request):
    return render(request, 'lg/dashboard2.html')


# @check_login
@locked
def my_course(request):
    tea_id = request.session['user_id']
    print(id)
    grade_list = Grade.objects.filter(teacher=tea_id)
    course_id = grade_list[0].id
    if 'id' in request.GET:
        course_id = request.GET.get('id')
    course = Grade.objects.get(id=course_id).course.all()
    tea = RegisterFirst.objects.filter(id=tea_id)[0]
    print(tea)
    print(grade_list)
    print(course)

    return render(request, 'lg/ui-buttons.html', locals())


# @check_login
@locked
def validation(request):
    userid = request.session['user_id']
    tea = RegisterFirst.objects.filter(id=userid)[0]
    id = request.GET.get('id')
    # print(id)
    teachers = RegisterFirst.objects.filter(deptotea__id=id)
    print(teachers)
    # teachers = list(DepToTea.objects.filter(department__id=id).values('id', 'teacher__username', 'teacher__id'))
    # print(teachers)
    # teachers = RegisterFirst.objects.filter(id=id)
    if teachers:
        teacher = teachers[0]
        print()
    return render(request, 'lg/form-validation.html', locals())


# @check_login
@locked
def xeditable(request):
    id = request.session['user_id']
    tea = RegisterFirst.objects.filter(id=id)[0]
    peple = DepToTea.objects.all()
    # tea = Teacher.objects.filter(user_id=1)
    print(peple[0].teacher)
    return render(request, 'lg/form-xeditable.html', locals())


# @check_login
@locked
def calendar(request):
    return render(request, 'lg/calendar.html')


# @check_login
@locked
def flot_chart(request):
    return render(request, 'lg/flot-chart.html')


# @check_login
@locked
def check_day(request):
    return render(request, 'lg/check_day.html')


# @check_login
@locked
def check_week(request):
    return render(request, 'lg/timeline.html')


# @check_login
@locked
def inform_filed(request):
    return render(request, 'lg/inform-filed.html')


# @check_login
@locked
def forgot_password(request):
    return render(request, 'lg/forgot-password.html')


# @check_login
@locked
def user_info(request):
    if request.method == 'GET':
        return render(request, 'lg/user_info.html')
    else:
        return render(request, 'lg/user_info.html')


# @check_login
@locked
def course_info(request):
    return render(request, 'lg/course_info.html')


#
# @check_login
# @locked
# def test(request):
#     return render(request, 'lg/test.html')

# @check_login
@locked
def del_cookie(request):
    response = HttpResponse('quit')
    try:
        response.delete_cookie('username')
        request.session.flush()
    except Exception as e:
        return render(request, 'lg/error-500.html', {'error': e})
    return response


# @check_login
@locked
def settings(request):
    return render(request, 'lg/settings.html')


# @check_login
@locked
def registration(request):
    return render(request, 'lg/registration.html')


# @check_login
@locked
def reset_pwd(request):
    return render(request, 'lg/reset-password.html')


# @check_login
@locked
def unlock(request):
    if request.method == 'GET':
        return render(request, 'lg/unlocked.html')
    else:
        pwd = request.POST.get('unpwd')
        request.session['unlock'] = pwd
        request.session['active'] = '0'
        return redirect('locked.html')


# @check_login
def locked(request):
    if request.method == 'GET':
        return render(request, 'lg/locked.html')
    else:
        pwd = request.POST.get('unpwd')
        if pwd == request.session['unlock']:
            request.session['active'] = '1'
            return redirect('index.html')
        else:
            msg = "解锁失败, 请输入正确密码!"
            return render(request, 'lg/locked.html', locals())
