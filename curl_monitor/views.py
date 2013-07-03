#coding: utf-8

from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.db import transaction
import os
import json


def get_monitor_list(request):
    monitor_list = MonitorItem.objects.all()
    monitor_dict_list = []
    for monitor in monitor_list:
        monitor_dict_list.append({
            "id": monitor.id,
            "url": monitor.url,
            "error_count": monitor.error_count,
            "last_status": monitor.last_status,
            "monitor_or_not": monitor.monitor_or_not,
            "ip_list":  monitor.ip_list.split(';')
        })
    return render(request, 'curl_monitor/monitor_list.html',
                  {'monitor_list': monitor_dict_list}
    )


@transaction.commit_manually
def del_monitor(request):
    id = request.GET['id']

    return_dict = {}
    try:
        MonitorItem.objects.filter(id=id).delete()
        MonitorLog.objects.filter(monitor_id=id).delete()
    except:
        transaction.rollback()
        return_dict['status'] = 'failure'
        return_dict['msg'] = u'数据库操作失败'
    else:
        transaction.commit()
        return_dict['status'] = 'success'

    return HttpResponse(json.dumps(return_dict))


def add_monitor(request):
    url = request.POST['url_to_monitor']
    ips = request.POST['ips']
    monitor_or_not = request.POST['monitor_or_not']

    return_dict = {}
    try:
        MonitorItem.objects.create(url=url, ip_list=ips, monitor_or_not=monitor_or_not)
    except:
        return_dict['status'] = 'failure'
        return_dict['msg'] = u'数据库操作失败'
    else:
        return_dict['status'] = 'success'

    return HttpResponse(json.dumps(return_dict))


def modify_monitor(request):
    id = request.POST['id']
    url_to_monitor = request.POST['url_to_monitor']
    ips = request.POST['ips']
    monitor_or_not = request.POST['monitor_or_not']

    return_dict = {}
    try:
        MonitorItem.objects.filter(id=id).update(url=url_to_monitor, ip_list=ips, monitor_or_not=monitor_or_not)
    except:
        return_dict['status'] = 'failure'
        return_dict['msg'] = u'数据库操作失败'
    else:
        return_dict['status'] = 'success'

    return HttpResponse(json.dumps(return_dict))

def get_log_list(request):
    monitor_id = request.GET['id']
    log_list = MonitorLog.objects.filter(monitor_id=monitor_id)
    return render(request, 'curl_monitor/log_list.html', {'log_list': log_list})


def get_log_content(request):
    id = request.GET['id']
    log_item = MonitorLog.objects.get(id=id)
    log_path = log_item.log_path

    if not os.path.exists(log_path):
        log_content = u'未找到该日志文件'
    else:
        with open(log_path, 'r') as fh:
            log_content = fh.read()
            log_content = log_content.replace('\n', '<br />')
    return HttpResponse(log_content)