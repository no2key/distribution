#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-13 上午9:58
# **************************************

import os
import time
import paramiko
from celery.task import task
from celery.result import AsyncResult


@task
def invoke_shell(shell_path):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('192.168.2.140', 36000, username='Administrator')
    #client.connect('192.168.2.237', 22, username='root', password='redhat')
    _, out, _ = client.exec_command(shell_path)
    output = []
    f_name = 'log/log_%s' % time.time()
    f = open(f_name, 'w')
    for line in out:
        f.write(line)
        if len(output) > 19:
            output.pop(0)
        output.append(line)
    f.close()
    output.append("Log file: /home/distribution/%s" % f_name)
    result = ''.join(output)
    return result


@task
def invoke_shell_local(shell_path):
    os.system(shell_path)
    return


def get_result(id_):
    result = AsyncResult(id_)
    return result
