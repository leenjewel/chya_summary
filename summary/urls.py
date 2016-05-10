from django.conf.urls import url
from . import views

app_name = 'summary'
urlpatterns = [
    url(r'^$', views.workbook, name = 'index'),
    url(r'^login/$', views.login, name = 'login'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^logout/$', views.logout, name = 'logout'),
    url(r'^workbook/$', views.workbook, name = 'workbook'),
    url(r'^sheet/([^\/]*)/$', views.sheet, name = 'sheet'),
    url(r'^table/([^\/]*)/([^\/]*)/$', views.table, name = 'table'),
]

