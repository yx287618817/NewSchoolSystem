
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^table-static.html/$', views.table_static),
    url(r'^table-responsive.html/$', views.table_responsive),
    url(r'^table-datatable.html/$', views.table_datatable),
    url(r'^message-view.html/$', views.message_view),
    url(r'^compose.html/$', views.compose_view),
    url(r'^inbox.html/$', views.inbox_view),
    url(r'^dashboard.html/$', views.dashboard2),
    url(r'^my_course.html/$', views.my_course),
    url(r'^form-validation.html/$', views.validation),
    url(r'^form-xeditable.html/$', views.xeditable),
    url(r'^flot-chart.html/$', views.flot_chart),
    url(r'^check-day.html/$', views.check_day),
    url(r'^check-week.html/$', views.check_week),
    url(r'^unlocked.html/$', views.unlock),
    url(r'^locked.html/$', views.lockeds),
    url(r'^user_info.html/$', views.user_info),
    url(r'^course_info.html/$', views.course_info),
    url(r'^test/$', views.test),
]
