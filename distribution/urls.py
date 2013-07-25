<<<<<<< HEAD
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dist import auth

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', auth.login),
    url(r'^accounts/logout/$', auth.logout),

    url(r'', include('dist.urls')),

    url(r'^curl/monitor_list/$', 'curl_monitor.views.get_monitor_list'),
    url(r'^curl/add_monitor/$', 'curl_monitor.views.add_monitor'),
    url(r'^curl/del_monitor/$', 'curl_monitor.views.del_monitor'),
    url(r'^curl/modify_monitor/$', 'curl_monitor.views.modify_monitor'),
    url(r'^curl/view_log_list/$', 'curl_monitor.views.get_log_list'),
    url(r'^curl/view_log/$', 'curl_monitor.views.get_log_content'),
)
=======
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dist import auth

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', auth.login),
    url(r'^accounts/logout/$', auth.logout),

    url(r'', include('dist.urls')),

    url(r'^curl/', include('curl_monitor.urls')),
)
>>>>>>> 1cab5b5bd2c27b7751579bc34333bc3c51e66be5
