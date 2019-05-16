from django.contrib import admin
from . import models


# 权限管理
# admin.site.register(models.Permission)
# admin.site.register(models.TablePermission)
# admin.site.register(models.TableName)
# admin.site.register(models.GroupPermission)
# admin.site.register(models.NoPermission)

# 多选管理
# admin.site.register(models.Grades)
# admin.site.register(models.Classes)
# admin.site.register(models.Sex)
# admin.site.register(models.StudentType)
# admin.site.register(models.StudentStatus)
# admin.site.register(models.Major)
# admin.site.register(models.RegisterTwo)
# admin.site.register(models.ClassSelect)
#
# admin.site.register(models.RegisterFirst)


@admin.register(models.DepToTea)
class Dep(admin.ModelAdmin):
    list_display = [
        'department',
        'teacher'
    ]

    # filter_horizontal = ['teacher']



# @admin.register(models.Department)
# class Dep(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'dep_name',
#     ]
#     list_filter = ['dep_name']


@admin.register(models.Work_state)
class Wstate(admin.ModelAdmin):
    list_display = [
        'id',
        'state_name',
    ]
    list_filter = ['state_name']


@admin.register(models.Work_arrange)
class Warrange(admin.ModelAdmin):
    list_display = [
        'id',
        'department',
        'tea_id',
        'title',
        'content',
        'work_type',
        'work_state',
        'date',
        'finish'
    ]

    list_filter = ['work_type']
    # 设置某个字段点击可以进入编辑页面
    list_display_links = ['id','department']


@admin.register(models.Work_type)
class WorkT(admin.ModelAdmin):
    list_display = [
        'id',
        'type_name',
    ]
    list_filter = ['type_name']
#
@admin.register(models.Course)
class Course_Admin(admin.ModelAdmin):
    list_display = [
        'id',
        'course_name',
    ]

    list_filter = [
        'course_name'
    ]
    list_display_links = [
        'id',
        'course_name'
    ]

@admin.register(models.Grade)
class Grade_Admin(admin.ModelAdmin):
    def show_mtm(self,grade):
        return [a.name for a in grade.course.all()]

    list_display = [
        'id',
        'grade_name',
        'department',

    ]

    filter_horizontal = ['course', 'teacher']

    list_filter = [
        'grade_name'
    ]

    list_display_links = [
        'id',
        'grade_name',
        'department',
    ]


# @admin.register(models.Inform)
# class Inform(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'send_from_tea',
#         'send_from_dpt',
#         'send_to_dpt',
#         'send_to_tea',
#         'title',
#         'filed_name',
#         'local_file',
#         'times',
#         'isActive',
#     ]
#     list_filter = [
#         'send_from_tea',
#         'send_from_dpt',
#         'title',
#     ]

    # list_display_links = [
    #     'id',
    #     'send_from_tea',
    #     'send_from_dpt',
    #     'send_to_dpt',
    #     'send_to_tea',
    #     'title',
    #     'filed_name',
    #     'times'
    # ]


@admin.register(models.Education)
class Edu_Admin(admin.ModelAdmin):
    list_display = [
        'id',
        'education',
    ]

    list_filter = ['education']
    list_display_links = ['education']

