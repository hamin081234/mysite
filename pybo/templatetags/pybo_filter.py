"""
파일명 : pybo_filter.py
설 명 : 
생성일 : 2023-02-03
생성자 : hamin
since 2023.01.09 Copyright (C) by Hamin All right reserved.
"""

from django import template

register = template.Library()


@register.filter
def sub(value, arg):
    """ 빼기 필터 """
    return value-arg
