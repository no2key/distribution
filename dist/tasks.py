#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-13 上午9:58
# **************************************

import os
import re
import datetime
import paramiko
from celery.task import task
from celery.result import AsyncResult


@task
def invoke_shell_remote(shell_path, event=None, ip='192.168.2.140', port=36000, username='Administrator', password=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username, password)
    _, out, _ = client.exec_command(shell_path)
    output = []
    f_name = 'log/log_%s' % datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d_%H-%M-%S")
    f = open(f_name, 'w')
    for line in out:
        f.write(line)
        if len(output) > 19:
            output.pop(0)
        output.append(line)
    f.close()
    output.append("Log file: /home/distribution/%s" % f_name)
    if event:
        # For Push Online
        event.push_log_name = "/home/distribution/" + f_name
        event.save()
    result = ''.join(output)
    return result


@task
def invoke_shell_local(shell_path, event=None):
    out = os.popen(shell_path)
    output = []
    f_name = 'log/log_%s' % datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d_%H-%M-%S")
    f = open(f_name, 'w')
    for line in out:
        f.write(line)
        if len(output) > 19:
            output.pop(0)
        output.append(line)
    f.close()
    output.append("Log file: /home/distribution/%s" % f_name)
    if event:
        # For SVN Checkout
        f = open(f_name, 'r')
        content = f.read()
        versions = re.findall('At revision (\d+)', content)
        if len(versions) == 2:
            re_code = versions[0]
            re_config = versions[1]
            event.pull_code_to = re_code
            event.pull_config_to = re_config
            event.pull_log_name = "/home/distribution/" + f_name
            event.save()
    result = ''.join(output)
    return result


def get_result(id_):
    result = AsyncResult(id_)
    return result


def invoke_local_shell_no_task(shell):
    out = os.popen(shell)
    return out.read()