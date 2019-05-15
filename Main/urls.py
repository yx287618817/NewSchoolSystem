from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^student_menu/$', views.student_menu, name='student_menu.html'),
    url(r'^$', views.login, name='login.html'),
    url(r'^login/$', views.login, name='login.html'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^manage_add/$', views.manage_add),
    url(r'^register_one/$', views.Register.register_one),
    url(r'^register_two/$', views.Register.register_two),
    url(r'^register_three/$', views.Register.register_three),
    url(r'^register_four/$', views.Register.register_four),
    url(r'^update_user_photo/$', views.update_user_photo),
    url(r'^sms_verification/$', views.sms_verification),
    url(r'^forget_passwd/$', views.forget_passwd),
]
