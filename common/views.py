import logging

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from common.forms import UserForm
from django.contrib.auth import authenticate, login


# Create your views here.

def signup(request):
    form = None
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():  # form이 유요할 경우
            # 회원가입
            form.save()
            # form username, password1
            username = form.cleaned_data.get('username')
            logging.info("username:{}".format(username))

            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            # 로그인
            user = authenticate(username=username, password=password1)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
