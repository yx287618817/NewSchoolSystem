from django.contrib import admin
from Main import models


# 权限管理
admin.site.register(models.Permission)
admin.site.register(models.TablePermission)
admin.site.register(models.TableName)
admin.site.register(models.GroupPermission)
admin.site.register(models.NoPermission)

# 多选管理
admin.site.register(models.Grades)
admin.site.register(models.Classes)
admin.site.register(models.Sex)
admin.site.register(models.StudentType)
admin.site.register(models.StudentStatus)
admin.site.register(models.Major)
admin.site.register(models.RegisterTwo)
admin.site.register(models.ClassSelect)
