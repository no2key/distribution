#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-13 上午9:58
# **************************************

import os
import paramiko
from celery.task import task
from celery.result import AsyncResult


@task
def invoke_shell(shell_path):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #client.connect('192.168.2.140', 36000, username='Administrator')
    client.connect('192.168.2.237', 22, username='root', password='redhat')
    _, out, _ = client.exec_command(shell_path)
    output = []
    for line in out:
        if len(output) > 9:
            output.pop(0)
        output.append(line)
    result = ''.join(output)
    return result


@task
def invoke_shell_local(shell_path):
    os.system(shell_path)
    return


def get_result(id_):
    result = AsyncResult(id_)
    return result
