#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-6-20 下午3:44
# **************************************

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render


class LoginForm(forms.Form):
    username = forms.CharField(label=u"用户名", max_length=30, widget=forms.TextInput(attrs={'size': 20,}))
    password = forms.CharField(label=u"密码", max_length=30, widget=forms.PasswordInput(attrs={'size': 20,}))


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST.copy())
        if form.is_valid():
            _login(request, form.cleaned_data["username"], form.cleaned_data["password"])
            return HttpResponseRedirect("/")
    return render(request, "dist/login.html", {'form': form})


def _login(request,username,password):
    ret = False
    user = authenticate(username=username,password=password)
    if user:
        if user.is_active:
            auth_login(request,user)
            ret = True
        else:
            messages.error(request, "用户未启用。")
    else:
        messages.error(request, "登录失败，请检查用户名密码。")
    return ret


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")