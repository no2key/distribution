#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-9 上午10:22
# **************************************

import time
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from distribution.settings import SVN_PREFIX, SVN_PASSWORD, SVN_USERNAME
from dist.tasks import invoke_shell
from dist.models import *


@login_required
def distribution(request):
    services = Service.objects.all()
    return render(request, 'service_distribution.html', {'services': services})


@login_required
def svn_pull(request, pk):
    service = get_object_or_404(Service, pk=pk)
    svn_config = SVN_PREFIX + '/config/' + service.svn_config_path
    svn_code = SVN_PREFIX + '/code/' + service.svn_package_path
    prepare_temp_dir = "DATE=`date +%s`; " \
                       "mkdir /cygdrive/e/Publish/svntemp/svn_tmp_$DATE/; " \
                       "mkdir /cygdrive/e/Publish/svntemp/svn_tmp_$DATE/code/; " \
                       "mkdir /cygdrive/e/Publish/svntemp/svn_tmp_$DATE/config/;"
    checkout_config = "cd /cygdrive/e/Publish/svntemp/svn_tmp_$DATE/config/; " \
                      "/cygdrive/c/\"Program Files\"/TortoiseSVN/bin/svn checkout %s --username=%s --password=%s;" % \
                      (svn_config, SVN_USERNAME, SVN_PASSWORD)
    checkout_code = "cd /cygdrive/e/Publish/svntemp/svn_tmp_$DATE/code/; " \
                    "/cygdrive/c/\"Program Files\"/TortoiseSVN/bin/svn checkout %s --username=%s --password=%s;" % \
                    (svn_code, SVN_USERNAME, SVN_PASSWORD)
    chmod = "chmod -R 777 /cygdrive/e/Publish/svntemp/svn_tmp_$DATE;"
    code_destination = "rsync -av --exclude=.svn /cygdrive/e/Publish/svntemp/svn_tmp_$DATE/code/%s/ /cygdrive/e/Publish/%s/;" % \
                       (service.svn_package_path, service.execute_machine)
    config_destination = "rsync -av --exclude=.svn /cygdrive/e/Publish/svntemp/svn_tmp_$DATE/config/%s/ /cygdrive/e/Publish/%s/;" % \
                         (service.svn_config_path, service.execute_machine)
    clean = "rm -r /cygdrive/e/Publish/svntemp/svn_tmp_$DATE/;"
    svn_command = prepare_temp_dir + checkout_code + checkout_config + chmod + code_destination + config_destination #+ clean
    result = invoke_shell.delay(svn_command)
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
        t_people=request.user.username,
    )
    task.save()
    return HttpResponseRedirect('/task_queue/')


@login_required
def push_online(request, pk):
    service = get_object_or_404(Service, pk=pk)
    svc_push = "cd /cygdrive/e/Publish/tools/; pwd; ./" + service.svc_push + " 2>&1"
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
        t_people=request.user.username,
    )
    task.save()
    return HttpResponseRedirect('/task_queue/')


@login_required
def service_restart(request, pk):
    service = get_object_or_404(Service, pk=pk)
    svc_restart = "cd /cygdrive/e/Publish/tools/; pwd; ./" + service.svc_restart + " 2>&1"
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
        t_people=request.user.username,
    )
    task.save()
    return HttpResponseRedirect('/task_queue/')


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
