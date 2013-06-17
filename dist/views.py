#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-9 上午10:22
# **************************************


from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from dist.tasks import invoke_shell
from dist.models import *


def distribution(request):
    services = Service.objects.all()
    return render(request, 'service_distribution.html', {'services': services})


def svn_pull(request, pk):
    service = get_object_or_404(Service, pk=pk)
    svn_path = service.svn_config_path
    result = invoke_shell.delay(svn_path)
    if not result.result:
        m_result = ""
    else:
        m_result = result.result
    task = TaskModel(
        t_service=service,
        t_content="SVN拉取新版本",
        t_task_id=result.id,
        t_status=result.status,
        t_result=m_result,
        t_people="Test",
    )
    task.save()
    return HttpResponseRedirect('/task_queue/')


def push_online(request, pk):
    service = get_object_or_404(Service, pk=pk)
    svc_push = service.svc_push
    result = invoke_shell.delay(svc_push)
    if not result.result:
        m_result = ""
    else:
        m_result = result.result
    task = TaskModel(
        t_service=service,
        t_content="推送上线",
        t_task_id=result.id,
        t_status=result.status,
        t_result=m_result,
        t_people="Test",
    )
    task.save()
    return HttpResponseRedirect('/task_queue/')


def service_restart(request, pk):
    service = get_object_or_404(Service, pk=pk)
    svc_restart = service.svc_restart
    result = invoke_shell.delay(svc_restart)
    if not result.result:
        m_result = ""
    else:
        m_result = result.result
    task = TaskModel(
        t_service=service,
        t_content="重启服务",
        t_task_id=result.id,
        t_status=result.status,
        t_result=m_result,
        t_people="Test",
    )
    task.save()
    return HttpResponseRedirect('/task_queue/')


class TaskQueue(ListView):
    model = TaskModel
    context_object_name = "tasks"
    template_name = 'task_queue.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        queryset = TaskModel.objects.order_by('-t_time')
        return queryset


class ServiceList(ListView):
    model = Service
    context_object_name = 'svc'
    template_name = 'service_list.html'
    paginate_by = 10


class ServiceAdd(CreateView):
    model = Service
    template_name = 'service_add.html'
    success_url = '/service_list'


class ServiceEdit(UpdateView):
    model = Service
    template_name = 'service_edit.html'
    success_url = '/service_list'


class ServiceDelete(DeleteView):
    model = Service
    template_name = 'confirm_delete.html'
    success_url = '/service_list'


class ServiceCategoryList(ListView):
    model = ServiceCategory
    context_object_name = 'category'
    template_name = 'service_category_list.html'
    paginate_by = 10


class ServiceCategoryAdd(CreateView):
    model = ServiceCategory
    template_name = 'service_category_add.html'
    success_url = '/service_category_list'


class ServiceCategoryEdit(UpdateView):
    model = ServiceCategory
    template_name = 'service_category_edit.html'
    success_url = '/service_category_list'


class ServiceCategoryDelete(DeleteView):
    model = ServiceCategory
    template_name = 'confirm_delete.html'
    success_url = '/service_category_list'


class ServerList(ListView):
    model = Server
    context_object_name = 'server'
    template_name = 'server_list.html'
    paginate_by = 10


class ServerAdd(CreateView):
    model = Server
    template_name = 'server_add.html'
    success_url = '/server_list'


class ServerEdit(UpdateView):
    model = Server
    template_name = 'server_edit.html'
    success_url = '/server_list'


class ServerDelete(DeleteView):
    model = Server
    template_name = 'confirm_delete.html'
    success_url = '/server_list'
