#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-13 上午10:54
# **************************************

import json
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from dist.models import TaskModel, Service
from dist.tasks import get_result, verify_path


def refresh_task_queue(request):
    pending = list(TaskModel.objects.filter(t_status="PENDING"))
    started = list(TaskModel.objects.filter(t_status="STARTED"))
    items = pending + started
    for item in items:
        result = get_result(item.t_task_id)
        if not result.result:
            m_result = ""
        else:
            m_result = result.result
        item.t_status = result.status
        item.t_result = m_result
        item.save()
    return HttpResponse("ok")


def validate_service(request, pk):
    service = get_object_or_404(Service, pk=int(pk))
    obj = {
        'svn_package_path': 0,
        'svn_config_path': 0,
        'execute_machine': 0,
        'svc_push': 0,
        'svc_restart': 0,
    }
    if verify_path('SVN', "http://192.168.2.140:8080/svn/publish/code/%s" % service.svn_package_path) and service.svn_package_path != '--':
        obj['svn_package_path'] = 1
    if verify_path('SVN', "http://192.168.2.140:8080/svn/publish/config/%s" % service.svn_config_path) and service.svn_config_path != '--':
        obj['svn_config_path'] = 1
    if verify_path('File', "/cygdrive/e/Publish/%s" % service.execute_machine) and service.execute_machine != '--':
        obj['execute_machine'] = 1
    if verify_path('File', "/cygdrive/e/Publish/tools/%s" % service.svc_push) and service.svc_push != '--':
        obj['svc_push'] = 1
    if verify_path('File', "/cygdrive/e/Publish/tools/%s" % service.svc_restart) and service.svc_restart != '--':
        obj['svc_restart'] = 1
    return HttpResponse(json.dumps(obj))


class ajax_queue(ListView):
    model = TaskModel
    context_object_name = "tasks"
    template_name = 'dist/ajax_queue.html'
    paginate_by = 30

    def dispatch(self, request, *args, **kwargs):
        pending = list(TaskModel.objects.filter(t_status="PENDING"))
        started = list(TaskModel.objects.filter(t_status="STARTED"))
        items = pending + started
        for item in items:
            result = get_result(item.t_task_id)
            if not result.result:
                m_result = ""
            else:
                m_result = result.result
            item.t_status = result.status
            item.t_result = m_result
            item.save()
        return super(ajax_queue, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        queryset = TaskModel.objects.order_by('-t_time')
        return queryset