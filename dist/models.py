#coding:utf-8

from django.db import models


class Service(models.Model):
    svc_name = models.CharField(unique=True, max_length=100, verbose_name="服务名称")
    category = models.ForeignKey('ServiceCategory', verbose_name="服务分类")
    server_list = models.ManyToManyField('Server', related_name='ServerList')
    svn_package_path = models.CharField(max_length=500, verbose_name="SVN包路径")
    svn_config_path = models.CharField(max_length=500, verbose_name="SVN配置路径")
    execute_machine = models.CharField(max_length=500, verbose_name="发布机路径")
    svc_push = models.CharField(max_length=500, verbose_name="推送脚本路径")
    svc_restart = models.CharField(max_length=500, verbose_name="服务重启脚本路径")

    def __unicode__(self):
        return self.svc_name


class ServiceCategory(models.Model):
    category_name = models.CharField(max_length=100, verbose_name="分类名称")

    def __unicode__(self):
        return self.category_name


class Server(models.Model):
    ip = models.IPAddressField(unique=True)
    hostname = models.CharField(unique=True, max_length=100)
    service_root_path = models.CharField(max_length=500, blank=True, verbose_name="服务根目录")

    def __unicode__(self):
        return self.ip + "\t" + self.hostname


class SVN(models.Model):
    svn_name = models.CharField(unique=True, max_length=100, verbose_name="SVN名称")
    svn_root = models.CharField(max_length=500, verbose_name="SVN根目录")
    svn_user = models.CharField(max_length=100, verbose_name="用户名")
    svn_pass = models.CharField(max_length=100, verbose_name="密码")

    def __unicode__(self):
        return self.svn_name


class EventLog(models.Model):
    log_category = models.CharField(max_length=100, verbose_name="类型")
    log_people = models.CharField(max_length=100, verbose_name="操作人")
    log_time = models.DateTimeField(auto_now=True, verbose_name="操作时间")
    log_level = models.CharField(max_length=100, verbose_name="日志级别")
    log_content = models.CharField(max_length=1000, verbose_name="日志详情")

    def __unicode__(self):
        return self.log_content


class TaskModel(models.Model):
    t_service = models.ForeignKey('Service', verbose_name="服务")
    t_content = models.CharField(max_length=500, verbose_name="执行操作")
    t_task_id = models.CharField(max_length=50, verbose_name="任务ID")
    t_status = models.CharField(max_length=50, verbose_name="任务状态")
    t_result = models.CharField(max_length=500, verbose_name="执行结果")
    t_people = models.CharField(max_length=50, verbose_name="执行人")
    t_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.t_service + ": " + self.t_content