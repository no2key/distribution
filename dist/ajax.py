#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-13 上午10:54
# **************************************

from django.http import HttpResponse
from dist.models import TaskModel
from dist.tasks import get_result


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
