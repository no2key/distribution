#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-24 上午10:31
# **************************************

from distribution.settings import SVN_PREFIX, SVN_PASSWORD, SVN_USERNAME
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import re
from dist.tasks import invoke_shell_remote, invoke_shell_local, invoke_local_shell_no_task
from dist.models import *


@login_required
def svn_pull(request, pk):
    service = get_object_or_404(Service, pk=pk)
    old_code = "cd /home/svnroot/code/%s; svn info" % service.svn_package_path
    re_code = re.findall("Revision: (\d+)", invoke_local_shell_no_task(old_code))
    if re_code:
        re_code = re_code[0]
    else:
        re_code = "?"
    old_config = "cd /home/svnroot/config/%s; svn info" % service.svn_config_path
    re_config = re.findall("Revision: (\d+)", invoke_local_shell_no_task(old_config))
    if re_config:
        re_config = re_config[0]
    else:
        re_config = "?"
    update_code = "cd /home/svnroot/code/%s; svn update --username=%s --password=%s;" % \
                  (service.svn_package_path, SVN_USERNAME, SVN_PASSWORD)
    update_config = "cd /home/svnroot/config/%s; svn update --username=%s --password=%s;" % \
                    (service.svn_config_path, SVN_USERNAME, SVN_PASSWORD)
    chmod = "chmod -R 777 /home/svnroot/code/%s; chmod -R 777 /home/svnroot/config/%s;" % \
            (service.svn_package_path, service.svn_config_path)
    prepare_temp_dir = "DATE=`date +%s`; mkdir /home/code_config_merge/tmp_$DATE/; "
    code_merge = "rsync -av --exclude=.svn /home/svnroot/code/%s/ /home/code_config_merge/tmp_$DATE/;" % \
                 service.svn_package_path
    config_merge = "rsync -av --exclude=.svn /home/svnroot/config/%s/ /home/code_config_merge/tmp_$DATE/;" % \
                   service.svn_config_path
    rsync_140 = "rsync -e 'ssh -p 36000 -l Administrator' -azv --exclude=.svn" \
                " /home/code_config_merge/tmp_$DATE/ 192.168.2.140:/cygdrive/e/Publish/%s/;" % service.execute_machine
    clean = "rm -rf /home/code_config_merge/tmp_$DATE/;"
    svn_command = update_code + update_config + chmod + prepare_temp_dir + code_merge + config_merge + rsync_140 + clean
    event = EventPull(
        pull_service=service,
        pull_people=request.user.username,
        pull_code_from=re_code,
        pull_config_from=re_config,
    )
    result = invoke_shell_local.delay(svn_command, event)
    if not result.result:
        m_result = ""
    else:
        m_result = result.result
    task = TaskModel(
        t_service=service,
        t_content=u"SVN拉取新版本",
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
    local_code = "cd /home/svnroot/code/%s; svn info" % service.svn_package_path
    re_code = re.findall("Revision: (\d+)", invoke_local_shell_no_task(local_code))
    if re_code:
        re_code = re_code[0]
    else:
        re_code = "?"
    local_config = "cd /home/svnroot/config/%s; svn info" % service.svn_config_path
    re_config = re.findall("Revision: (\d+)", invoke_local_shell_no_task(local_config))
    if re_config:
        re_config = re_config[0]
    else:
        re_config = "?"
    svc_push = "cd /cygdrive/e/Publish/tools/; ./" + service.svc_push + " 2>&1"
    event = EventPush(
        push_service=service,
        push_people=request.user.username,
        push_code=re_code,
        push_config=re_config,
    )
    result = invoke_shell_remote.delay(
        shell_path=svc_push,
        event=event,
        ip='192.168.2.140',
        port=36000,
        username='Administrator'
    )
    if not result.result:
        m_result = ""
    else:
        m_result = result.result
    task = TaskModel(
        t_service=service,
        t_content=u"推送上线",
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
    result = invoke_shell_remote.delay(
        shell_path=svc_restart,
        ip='192.168.2.140',
        port=36000,
        username='Administrator'
    )
    if not result.result:
        m_result = ""
    else:
        m_result = result.result
    task = TaskModel(
        t_service=service,
        t_content=u"重启服务",
        t_task_id=result.id,
        t_status=result.status,
        t_result=m_result,
        t_people=request.user.username,
    )
    task.save()
    return HttpResponseRedirect('/task_queue/')


def service_independent(request):
    service = get_object_or_404(Service, svc_name='Z_Independent_Scripts')
    script_name = request.POST['script']
    script_to_run = "cd /cygdrive/e/Publish/tools/; ./" + script_name + " 2>&1"
    result = invoke_shell_remote.delay(
        shell_path=script_to_run,
        ip='192.168.2.140',
        port=36000,
        username='Administrator'
    )
    #result = invoke_shell_remote.delay("/home/test.sh", ip='192.168.2.237', port=22, username='root', password='redhat')
    if not result.result:
        m_result = ""
    else:
        m_result = result.result
    task = TaskModel(
        t_service=service,
        t_content=u"执行独立脚本: /cygdrive/e/Publish/tools/%s" % script_name,
        t_task_id=result.id,
        t_status=result.status,
        t_result=m_result,
        t_people=request.user.username,
    )
    task.save()
    return
