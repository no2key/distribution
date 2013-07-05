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
