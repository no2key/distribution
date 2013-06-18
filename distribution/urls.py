from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dist import views, ajax

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'distribution.views.home', name='home'),
    # url(r'^distribution/', include('distribution.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.distribution, name='index'),
    url(r'service_distribution/', views.distribution, name='service_distribution'),
    url(r'svn_pull/(?P<pk>\d+)', views.svn_pull, name='svn_pull'),
    url(r'push_online/(?P<pk>\d+)', views.push_online, name='push_online'),
    url(r'service_restart/(?P<pk>\d+)', views.service_restart, name='service_restart'),
    url(r'task_queue/', views.TaskQueue.as_view(), name='task_queue'),
    url(r'refresh_queue/', ajax.refresh_task_queue, name='refresh_queue'),
    url(r'ajax_queue/', ajax.ajax_queue.as_view(), name='ajax_queue'),

    url(r'service_add/', views.ServiceAdd.as_view(), name='service_add'),
    url(r'service_edit/(?P<pk>\d+)', views.ServiceEdit.as_view(), name='service_edit'),
    url(r'service_list/', views.ServiceList.as_view(), name='service_list'),
    url(r'service_delete/(?P<pk>\d+)', views.ServiceDelete.as_view(), name='service_delete'),

    url(r'service_category_add/', views.ServiceCategoryAdd.as_view(), name='service_category_add'),
    url(r'service_category_edit/(?P<pk>\d+)', views.ServiceCategoryEdit.as_view(), name='service_category_edit'),
    url(r'service_category_list/', views.ServiceCategoryList.as_view(), name='service_category_list'),
    url(r'service_category_delete/(?P<pk>\d+)', views.ServiceCategoryDelete.as_view(), name='service_category_delete'),

    url(r'server_add/', views.ServerAdd.as_view(), name='server_add'),
    url(r'server_edit/(?P<pk>\d+)', views.ServerEdit.as_view(), name='server_edit'),
    url(r'server_list/', views.ServerList.as_view(), name='server_list'),
    url(r'server_delete/(?P<pk>\d+)', views.ServerDelete.as_view(), name='server_delete'),

)
