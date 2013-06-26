#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-24 上午10:31
# **************************************

from distribution.settings import SVN_PREFIX, SVN_PASSWORD, SVN_USERNAME
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from dist.tasks import invoke_shell
from dist.models import *


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
    code_destination = "rsync -av --exclude=.svn /cygdrive/e/Publish/svntemp/svn_tmp_$DATE/code/%s/ " \
                       "/cygdrive/e/Publish/%s/;" % (service.svn_package_path, service.execute_machine)
    config_destination = "rsync -av --exclude=.svn /cygdrive/e/Publish/svntemp/svn_tmp_$DATE/config/%s/ " \
                         "/cygdrive/e/Publish/%s/;" % (service.svn_config_path, service.execute_machine)
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
    svc_push = "cd /cygdrive/e/Publish/tools/; ./" + service.svc_push + " 2>&1"
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
    svc_restart = "cd /cygdrive/e/Publish/tools/; ./" + service.svc_restart + " 2>&1"
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


@login_required
def service_independent(request):
    service = get_object_or_404(Service, svc_name='Z_Independent_Scripts')
    script_name = request.POST['script']
    script_to_run = "cd /cygdrive/e/Publish/tools/; ./" + script_name + " 2>&1"
    result = invoke_shell.delay(script_to_run)
    if not result.result:
        m_result = ""
    else:
        m_result = result.result
    task = TaskModel(
        t_service=service,
        t_content="执行独立脚本",
        t_task_id=result.id,
        t_status=result.status,
        t_result=m_result,
        t_people=request.user.username,
    )
    task.save()
    return HttpResponseRedirect('/task_queue/')
