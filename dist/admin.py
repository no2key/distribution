<<<<<<< HEAD
#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-9 上午9:52
# **************************************

from django.contrib import admin
from dist.models import *


class ServiceAdmin(admin.ModelAdmin):
    filter_horizontal = ('server_list', )


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceCategory)
admin.site.register(Server)
admin.site.register(SVN)
=======
#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-9 上午9:52
# **************************************

from django.contrib import admin
from dist.models import *


class ServiceAdmin(admin.ModelAdmin):
    filter_horizontal = ('server_list', )


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceCategory)
admin.site.register(Server)
admin.site.register(SVN)
>>>>>>> 1cab5b5bd2c27b7751579bc34333bc3c51e66be5
admin.site.register(EventLog)