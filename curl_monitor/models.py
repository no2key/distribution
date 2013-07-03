#coding: utf-8

from django.db import models


class MonitorLog(models.Model):
    monitor_id = models.IntegerField()
    log_path = models.CharField(max_length=250)
    date_time = models.DateTimeField(auto_now=True)


class MonitorItem(models.Model):
    url = models.CharField(max_length=1024)
    ip_list = models.TextField()
    error_count = models.IntegerField(default=0)
    last_status = models.CharField(max_length=1024, blank=True)
    monitor_or_not = models.BooleanField()