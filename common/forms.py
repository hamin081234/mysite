"""
파일명 : forms.py
설 명 : 
생성일 : 2023-02-06
생성자 : hamin
since 2023.01.09 Copyright (C) by Hamin All right reserved.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')
