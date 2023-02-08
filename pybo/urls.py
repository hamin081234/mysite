"""
파일명 : urls.py
설 명 : pybo 모든 URL과 view함수의 mapping 담당
생성일 : 2023-01-25
생성자 : hamin
since 2023.01.09 Copyright (C) by Hamin All right reserved.
"""
from django.urls import path

from . import views  # 현재디렉토리의 views 모듈
# from pybo import views

app_name = 'pybo'

urlpatterns =[
    path('', views.index, name="index"),
    path('<int:question_id>/', views.detail, name="detail"),

    # temp menu
    # path("boot/menu/", views.boot_menu, name="boot_menu"),

    # answer
    path('answer/create/<int:question_id>/', views.answer_create, name="answer_create"),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name="answer_delete"),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name="answer_modify"),

    # question
    path('register/', views.register, name="register"),
    path('question/modify/<int:question_id>/', views.modify_question, name="question_modify"),
    path('question/delete/<int:question_id>/', views.delete_question, name="question_delete"),
]
