#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-9 上午10:22
# **************************************

import os
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from dist.models import *
from execute import service_independent


@login_required
def distribution(request):
    services = Service.objects.all().order_by('svc_name')
    return render(request, 'service_distribution.html', {'services': services})


@login_required
def view_log(request):
    if request.method == "POST":
        f_name = 'log/%s' % request.POST['filename']
        try:
            f = open(f_name)
            log_content = f.read()
            f.close()
            import chardet
            log_encoding = chardet.detect(log_content)['encoding']
            log_content = log_content.decode(log_encoding)
            log_content = log_content.replace('\n', '<br />')
            return HttpResponse(log_content)
        except:
            return HttpResponse("ERROR OPENING %s" % f_name)
    else:
        LOGS = os.popen("ls log/")
        log_list = []
        for log in LOGS:
            log_list.append(log.strip())
        return render(request, 'view_log.html', {'logs': log_list})


@login_required
def independent_script(request):
    if request.method == "POST":
        if request.POST['script'] == '':
            error = "命令不能为空"
            return render(request, 'service_independent_script.html', {'error': error})
        service_independent(request)
        return HttpResponseRedirect("/task_queue/")
    else:
        return render(request, 'service_independent_script.html')


class TaskQueue(ListView):
    model = TaskModel
    context_object_name = "tasks"
    template_name = 'task_queue.html'
    paginate_by = 30

    def get_queryset(self, *args, **kwargs):
        queryset = TaskModel.objects.order_by('-t_time')
        return queryset


class ServiceList(ListView):
    model = Service
    queryset = Service.objects.order_by('svc_name')
    context_object_name = 'svc'
    template_name = 'service_list.html'
    paginate_by = 30


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
    paginate_by = 30


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
    paginate_by = 30


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
