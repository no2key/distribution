#coding:utf-8

from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'monitor_list/$', views.get_monitor_list),
    url(r'add_monitor/$', views.add_monitor),
    url(r'del_monitor/$', views.del_monitor),
    url(r'modify_monitor/$', views.modify_monitor),
    url(r'view_log_list/$', views.get_log_list),
    url(r'view_log/$', views.get_log_content),
)