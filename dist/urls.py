#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-7-3 下午3:46
# **************************************

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from dist import views, execute, ajax

urlpatterns = patterns('',

    url(r'^$', views.distribution, name='index'),
    url(r'service_distribution/', views.distribution, name='service_distribution'),
    url(r'script_execution/', views.script_execution, name='script_execution'),
    url(r'independent_script/', views.independent_script, name='independent_script'),
    url(r'task_queue/', login_required(views.TaskQueue.as_view()), name='task_queue'),
    url(r'refresh_queue/', ajax.refresh_task_queue, name='refresh_queue'),
    url(r'ajax_queue/', login_required(ajax.ajax_queue.as_view()), name='ajax_queue'),
    url(r'validate_service/(?P<pk>\d+)', ajax.validate_service, name="validate_service"),
    url(r'^view_log/', login_required(views.view_log), name='view_log'),

    url(r'svn_pull/(?P<pk>\d+)', execute.svn_pull, name='svn_pull'),
    url(r'push_online/(?P<pk>\d+)', execute.push_online, name='push_online'),
    url(r'service_restart/(?P<pk>\d+)', execute.service_restart, name='service_restart'),

    url(r'service_add/', login_required(views.ServiceAdd.as_view()), name='service_add'),
    url(r'service_edit/(?P<pk>\d+)', login_required(views.ServiceEdit.as_view()), name='service_edit'),
    url(r'service_list/', login_required(views.ServiceList.as_view()), name='service_list'),
    url(r'service_delete/(?P<pk>\d+)', login_required(views.ServiceDelete.as_view()), name='service_delete'),

    url(r'script_add/', login_required(views.ScriptAdd.as_view()), name='script_add'),
    url(r'script_edit/(?P<pk>\d+)', login_required(views.ScriptEdit.as_view()), name='script_edit'),
    url(r'script_list/', login_required(views.ScriptList.as_view()), name='script_list'),
    url(r'script_delete/(?P<pk>\d+)', login_required(views.ScriptDelete.as_view()), name='script_delete'),

    url(r'service_category_add/', login_required(views.ServiceCategoryAdd.as_view()), name='service_category_add'),
    url(r'service_category_edit/(?P<pk>\d+)', login_required(views.ServiceCategoryEdit.as_view()), name='service_category_edit'),
    url(r'service_category_list/', login_required(views.ServiceCategoryList.as_view()), name='service_category_list'),
    url(r'service_category_delete/(?P<pk>\d+)', login_required(views.ServiceCategoryDelete.as_view()), name='service_category_delete'),

    url(r'server_add/', login_required(views.ServerAdd.as_view()), name='server_add'),
    url(r'server_edit/(?P<pk>\d+)', login_required(views.ServerEdit.as_view()), name='server_edit'),
    url(r'server_list/', login_required(views.ServerList.as_view()), name='server_list'),
    url(r'server_delete/(?P<pk>\d+)', login_required(views.ServerDelete.as_view()), name='server_delete'),

    url(r'event_pull_list/', login_required(views.EventPullList.as_view()), name='event_pull_list'),
    url(r'event_push_list/', login_required(views.EventPushList.as_view()), name='event_push_list'),

)