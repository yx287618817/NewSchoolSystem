
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^table-static.html/$', views.table_static),
    url(r'^table-responsive.html/$', views.table_responsive),
    url(r'^table-datatable.html/$', views.table_datatable),
    url(r'^message-view.html/$', views.message_view),
    url(r'^inbox.html/$', views.inbox_view),
    # url(r'^compose.html/$', views.compose_view),
    url(r'^logout/$', views.logout),
    url(r'^dashboard2.html/$', views.dashboard2),
    url(r'^my_course.html/$', views.my_course),
    url(r'^form-validation.html/$', views.validation),
    url(r'^form-xeditable.html/$', views.xeditable),
    url(r'^calendar.html/$', views.calendar),
    url(r'^flot-chart.html/$', views.flot_chart),
    url(r'^check-day.html/$', views.check_day),
    url(r'^check-week.html/$', views.check_week),
    url(r'^inform-filed.html/$', views.inform_filed),
    url(r'^forgot-password.html/$', views.forgot_password),
    url(r'^unlocked.html/$', views.unlock),
    url(r'^locked.html/$', views.locked),
    url(r'^user_info.html/$', views.user_info),
    url(r'^course_info.html/$', views.course_info),
    url(r'^widget.html$', views.settings),
    url(r'^registration.html/$', views.registration),
    url(r'^reset-password.html/$', views.reset_pwd),
    url(r'^reset-password.html/$', views.reset_pwd),
]