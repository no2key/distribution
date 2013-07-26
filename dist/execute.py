#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-24 上午10:31
# **************************************

from distribution.settings import SVN_PREFIX, SVN_PASSWORD, SVN_USERNAME
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import Context
from django.template.loader import get_template
import re
import datetime
from dist.tasks import invoke_shell_remote, invoke_shell_local, invoke_shell_local_no_task
from dist.models import *


def get_revnum(code_or_config, path):
    shell_str = "cd /home/svnroot/%s/%s; svn info" % (code_or_config, path)
    revnum = re.findall("Revision: (\d+)", invoke_shell_local_no_task(shell_str))
    if revnum:
        revnum = revnum[0]
    else:
        revnum = "?"
    return revnum


def get_runshell(src_name):
    return "cd /cygdrive/e/Publish/tools/; ./" + src_name + " 2>&1"


@login_required
def svn_pull(request, pk):
    service = get_object_or_404(Service, pk=pk)
    r = request.POST.get("r", None)
    re_code = get_revnum("code", service.svn_package_path)
    re_config = get_revnum("config", service.svn_config_path)
    n_now = datetime.datetime.now()
    now_str = n_now.strftime("%Y-%m-%d_%H-%M-%S")
    c = Context({
        "svn_package_path": service.svn_package_path,
        "svn_config_path": service.svn_config_path,
        "username": SVN_USERNAME,
        "password": SVN_PASSWORD,
        "prefix": SVN_PREFIX,
        "execute_machine": service.execute_machine,
        "date": now_str,
    })
    if r is not None:
        content = u"版本回退"
        c['r'] = r
        t = get_template("dist/shell/svn_roll_back.sh")
    else:
        content = u"SVN拉取新版本"
        t = get_template("dist/shell/svn_pull.sh")
    svn_command = t.render(c)
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
        t_content=content,
        t_task_id=result.id,
        t_status=result.status,
        t_result=m_result,
        t_people=request.user.username,
    )
    task.save()
    return HttpResponseRedirect(reverse("task_queue"))


@login_required
def push_online(request, pk):
    service = get_object_or_404(Service, pk=pk)
    re_code = get_revnum("code", service.svn_package_path)
    re_config = get_revnum("config", service.svn_config_path)
    svc_push = get_runshell(service.svc_push)
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
    return HttpResponseRedirect(reverse("task_queue"))


@login_required
def service_restart(request, pk):
    service = get_object_or_404(Service, pk=pk)
    svc_restart = get_runshell(service.svc_restart)
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
    return HttpResponseRedirect(reverse("task_queue"))


def service_independent(request):
    service = get_object_or_404(Service, svc_name='Z_Independent_Scripts')
    script_name = request.POST['script']
    script_to_run = get_runshell(script_name)
    result = invoke_shell_remote.delay(
        shell_path=script_to_run,
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
        t_content=u"执行独立脚本: /cygdrive/e/Publish/tools/%s" % script_name,
        t_task_id=result.id,
        t_status=result.status,
        t_result=m_result,
        t_people=request.user.username,
    )
    task.save()
    return
