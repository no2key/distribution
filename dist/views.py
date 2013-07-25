<<<<<<< HEAD
#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-9 上午10:22
# **************************************

import os
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm, forms
from dist.models import *
from execute import service_independent
from tasks import verify_path


@login_required
def distribution(request):
    services = Service.objects.all().order_by('svc_name')
    return render(request, 'dist/service_distribution.html', {'services': services})


@login_required
def script_execution(request):
    script = Script.objects.all().order_by('script_name')
    return render(request, 'dist/script_execution.html', {'script': script})


@login_required
def view_log(request):
    if request.method == "POST":
        f_name = 'log/%s' % request.POST['filename']
        try:
            f = open(f_name)
            log_content = f.read()
            f.close()
            import chardet
            log_encoding = chardet.detect(log_content)['encoding']
            log_content = log_content.decode(log_encoding)
            log_content = log_content.replace('\n', '<br />')
            return HttpResponse(log_content)
        except:
            return HttpResponse("ERROR OPENING %s" % f_name)
    else:
        LOGS = os.popen("ls log/")
        log_list = []
        for log in LOGS:
            log_list.append(log.strip())
        return render(request, 'dist/view_log.html', {'logs': log_list})


@login_required
def independent_script(request):
    if request.method == "POST":
        if request.POST['script'] == '':
            error = "命令不能为空"
            return render(request, 'dist/service_independent_script.html', {'error': error})
        service_independent(request)
        return HttpResponseRedirect(reverse("task_queue"))
    else:
        return render(request, 'dist/service_independent_script.html')


class TaskQueue(ListView):
    model = TaskModel
    context_object_name = "tasks"
    template_name = 'dist/task_queue.html'
    paginate_by = 50

    def get_queryset(self, *args, **kwargs):
        queryset = TaskModel.objects.order_by('-t_time')
        return queryset


class ServiceForm(ModelForm):
    class Meta:
        model = Service

    def clean_svn_package_path(self):
        super(ServiceForm, self).clean()
        cd = self.cleaned_data
        if not verify_path('SVN', "http://192.168.2.140:8080/svn/publish/code/%s" % cd['svn_package_path']):
            raise forms.ValidationError("Code路径不存在")
        return cd['svn_package_path']

    def clean_svn_config_path(self):
        super(ServiceForm, self).clean()
        cd = self.cleaned_data
        if not verify_path('SVN', "http://192.168.2.140:8080/svn/publish/config/%s" % cd['svn_config_path']):
            raise forms.ValidationError("Config路径不存在")
        return cd['svn_config_path']

    def clean_execute_machine(self):
        super(ServiceForm, self).clean()
        cd = self.cleaned_data
        if not verify_path('File', "/cygdrive/e/Publish/%s" % cd['execute_machine']):
            raise forms.ValidationError("发布机路径不存在")
        return cd['execute_machine']

    def clean_svc_push(self):
        super(ServiceForm, self).clean()
        cd = self.cleaned_data
        if not verify_path('File', "/cygdrive/e/Publish/tools/%s" % cd['svc_push']):
            raise forms.ValidationError("推送脚本不存在")
        return cd['svc_push']

    def clean_svc_restart(self):
        super(ServiceForm, self).clean()
        cd = self.cleaned_data
        if not verify_path('File', "/cygdrive/e/Publish/tools/%s" % cd['svc_restart']):
            raise forms.ValidationError("重启脚本不存在")
        return cd['svc_restart']


class ServiceList(ListView):
    model = Service
    queryset = Service.objects.order_by('svc_name')
    context_object_name = 'svc'
    template_name = 'dist/service_list.html'
    paginate_by = 50


class ServiceAdd(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'dist/service_add.html'

    def get_success_url(self):
        return reverse('service_list')


class ServiceEdit(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'dist/service_edit.html'

    def get_success_url(self):
        return reverse('service_list')


class ServiceDelete(DeleteView):
    model = Service
    template_name = 'dist/confirm_delete.html'

    def get_success_url(self):
        return reverse('service_list')


class ServiceCategoryList(ListView):
    model = ServiceCategory
    context_object_name = 'category'
    template_name = 'dist/service_category_list.html'
    paginate_by = 50


class ServiceCategoryAdd(CreateView):
    model = ServiceCategory
    template_name = 'dist/service_category_add.html'

    def get_success_url(self):
        return reverse('service_category_list')


class ServiceCategoryEdit(UpdateView):
    model = ServiceCategory
    template_name = 'dist/service_category_edit.html'

    def get_success_url(self):
        return reverse('service_category_list')


class ServiceCategoryDelete(DeleteView):
    model = ServiceCategory
    template_name = 'dist/confirm_delete.html'

    def get_success_url(self):
        return reverse('service_category_list')


class ServerList(ListView):
    model = Server
    context_object_name = 'server'
    template_name = 'dist/server_list.html'
    paginate_by = 50


class ServerAdd(CreateView):
    model = Server
    template_name = 'dist/server_add.html'

    def get_success_url(self):
        return reverse('server_list')


class ServerEdit(UpdateView):
    model = Server
    template_name = 'dist/server_edit.html'

    def get_success_url(self):
        return reverse('server_list')


class ServerDelete(DeleteView):
    model = Server
    template_name = 'dist/confirm_delete.html'

    def get_success_url(self):
        return reverse('server_list')

class ScriptList(ListView):
    model = Script
    context_object_name = 'script'
    template_name = 'dist/script_list.html'
    paginate_by = 50


class ScriptAdd(CreateView):
    model = Script
    template_name = 'dist/script_add.html'

    def get_success_url(self):
        return reverse('script_list')


class ScriptEdit(UpdateView):
    model = Script
    template_name = 'dist/script_edit.html'

    def get_success_url(self):
        return reverse('script_list')


class ScriptDelete(DeleteView):
    model = Script
    template_name = 'dist/confirm_delete.html'

    def get_success_url(self):
        return reverse('script_list')


class EventPullList(ListView):
    model = EventPull
    context_object_name = 'event_pull'
    template_name = 'dist/event_pull_list.html'
    paginate_by = 50


class EventPushList(ListView):
    model = EventPush
    context_object_name = 'event_push'
    template_name = 'dist/event_push_list.html'
=======
#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-9 上午10:22
# **************************************

import os
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm, forms
from dist.models import *
from execute import service_independent
from tasks import verify_path


@login_required
def distribution(request):
    services = Service.objects.all().order_by('svc_name')
    return render(request, 'dist/service_distribution.html', {'services': services})


@login_required
def script_execution(request):
    script = Script.objects.all().order_by('script_name')
    return render(request, 'dist/script_execution.html', {'script': script})


@login_required
def view_log(request):
    if request.method == "POST":
        f_name = 'log/%s' % request.POST['filename']
        try:
            f = open(f_name)
            log_content = f.read()
            f.close()
            import chardet
            log_encoding = chardet.detect(log_content)['encoding']
            log_content = log_content.decode(log_encoding)
            log_content = log_content.replace('\n', '<br />')
            return HttpResponse(log_content)
        except:
            return HttpResponse("ERROR OPENING %s" % f_name)
    else:
        LOGS = os.popen("ls log/")
        log_list = []
        for log in LOGS:
            log_list.append(log.strip())
        return render(request, 'dist/view_log.html', {'logs': log_list})


@login_required
def independent_script(request):
    if request.method == "POST":
        if request.POST['script'] == '':
            error = "命令不能为空"
            return render(request, 'dist/service_independent_script.html', {'error': error})
        service_independent(request)
        return HttpResponseRedirect(reverse("task_queue"))
    else:
        return render(request, 'dist/service_independent_script.html')


class TaskQueue(ListView):
    model = TaskModel
    context_object_name = "tasks"
    template_name = 'dist/task_queue.html'
    paginate_by = 50

    def get_queryset(self, *args, **kwargs):
        queryset = TaskModel.objects.order_by('-t_time')
        return queryset


class ServiceForm(ModelForm):
    class Meta:
        model = Service

    def clean_svn_package_path(self):
        super(ServiceForm, self).clean()
        cd = self.cleaned_data
        if not verify_path('SVN', "http://192.168.2.140:8080/svn/publish/code/%s" % cd['svn_package_path']):
            raise forms.ValidationError("Code路径不存在")
        return cd['svn_package_path']

    def clean_svn_config_path(self):
        super(ServiceForm, self).clean()
        cd = self.cleaned_data
        if not verify_path('SVN', "http://192.168.2.140:8080/svn/publish/config/%s" % cd['svn_config_path']):
            raise forms.ValidationError("Config路径不存在")
        return cd['svn_config_path']

    def clean_execute_machine(self):
        super(ServiceForm, self).clean()
        cd = self.cleaned_data
        if not verify_path('File', "/cygdrive/e/Publish/%s" % cd['execute_machine']):
            raise forms.ValidationError("发布机路径不存在")
        return cd['execute_machine']

    def clean_svc_push(self):
        super(ServiceForm, self).clean()
        cd = self.cleaned_data
        if not verify_path('File', "/cygdrive/e/Publish/tools/%s" % cd['svc_push']):
            raise forms.ValidationError("推送脚本不存在")
        return cd['svc_push']

    def clean_svc_restart(self):
        super(ServiceForm, self).clean()
        cd = self.cleaned_data
        if not verify_path('File', "/cygdrive/e/Publish/tools/%s" % cd['svc_restart']):
            raise forms.ValidationError("重启脚本不存在")
        return cd['svc_restart']


class ServiceList(ListView):
    model = Service
    queryset = Service.objects.order_by('svc_name')
    context_object_name = 'svc'
    template_name = 'dist/service_list.html'
    paginate_by = 50


class ServiceAdd(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'dist/service_add.html'

    def get_success_url(self):
        return reverse('service_list')


class ServiceEdit(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'dist/service_edit.html'

    def get_success_url(self):
        return reverse('service_list')


class ServiceDelete(DeleteView):
    model = Service
    template_name = 'dist/confirm_delete.html'

    def get_success_url(self):
        return reverse('service_list')


class ServiceCategoryList(ListView):
    model = ServiceCategory
    context_object_name = 'category'
    template_name = 'dist/service_category_list.html'
    paginate_by = 50


class ServiceCategoryAdd(CreateView):
    model = ServiceCategory
    template_name = 'dist/service_category_add.html'

    def get_success_url(self):
        return reverse('service_category_list')


class ServiceCategoryEdit(UpdateView):
    model = ServiceCategory
    template_name = 'dist/service_category_edit.html'

    def get_success_url(self):
        return reverse('service_category_list')


class ServiceCategoryDelete(DeleteView):
    model = ServiceCategory
    template_name = 'dist/confirm_delete.html'

    def get_success_url(self):
        return reverse('service_category_list')


class ServerList(ListView):
    model = Server
    context_object_name = 'server'
    template_name = 'dist/server_list.html'
    paginate_by = 50


class ServerAdd(CreateView):
    model = Server
    template_name = 'dist/server_add.html'

    def get_success_url(self):
        return reverse('server_list')


class ServerEdit(UpdateView):
    model = Server
    template_name = 'dist/server_edit.html'

    def get_success_url(self):
        return reverse('server_list')


class ServerDelete(DeleteView):
    model = Server
    template_name = 'dist/confirm_delete.html'

    def get_success_url(self):
        return reverse('server_list')

class ScriptList(ListView):
    model = Script
    context_object_name = 'script'
    template_name = 'dist/script_list.html'
    paginate_by = 50


class ScriptAdd(CreateView):
    model = Script
    template_name = 'dist/script_add.html'

    def get_success_url(self):
        return reverse('script_list')


class ScriptEdit(UpdateView):
    model = Script
    template_name = 'dist/script_edit.html'

    def get_success_url(self):
        return reverse('script_list')


class ScriptDelete(DeleteView):
    model = Script
    template_name = 'dist/confirm_delete.html'

    def get_success_url(self):
        return reverse('script_list')


class EventPullList(ListView):
    model = EventPull
    context_object_name = 'event_pull'
    template_name = 'dist/event_pull_list.html'
    paginate_by = 50


class EventPushList(ListView):
    model = EventPush
    context_object_name = 'event_push'
    template_name = 'dist/event_push_list.html'
>>>>>>> 1cab5b5bd2c27b7751579bc34333bc3c51e66be5
    paginate_by = 50