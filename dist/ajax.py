#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-13 上午10:54
# **************************************

from django.views.generic import ListView
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


class ajax_queue(ListView):
    model = TaskModel
    context_object_name = "tasks"
    template_name = 'ajax_queue.html'
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