"""
파일명 : urls.py
설 명 : pybo 모든 URL과 view함수의 mapping 담당
생성일 : 2023-01-25
생성자 : hamin
since 2023.01.09 Copyright (C) by Hamin All right reserved.
"""
from django.urls import path

from .views import base_views  # 현재디렉토리의 views 모듈
from .views import question_views
from .views import answer_views
# from pybo import views

app_name = 'pybo'

urlpatterns =[
    path('', base_views.index, name="index"),

    # temp menu
    # path("boot/menu/", views.boot_menu, name="boot_menu"),

    # answer
    path('answer/create/<int:question_id>/', answer_views.answer_create, name="answer_create"),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name="answer_delete"),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name="answer_modify"),
    path('answer/vote/<int:answer_id>/', answer_views.answer_vote, name="answer_vote"),

    # question
    path('register/', question_views.register, name="register"),
    path('<int:question_id>/', question_views.detail, name="detail"),
    path('question/modify/<int:question_id>/', question_views.modify_question, name="question_modify"),
    path('question/delete/<int:question_id>/', question_views.delete_question, name="question_delete"),
    path('question/vote/<int:question_id>/', question_views.vote_question, name="question_vote"),
]
