"""
파일명 : pybo_filter.py
설 명 : 
생성일 : 2023-02-03
생성자 : hamin
since 2023.01.09 Copyright (C) by Hamin All right reserved.
"""

from django import template
import markdown
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def mark(value):
    ''' 입력된 문자열을 html로 변화'''
    # nl2br (줄바꿈 문자-> <br>, fenced_code(마크다운))
    extensions = ['nl2br', 'fenced_code']
    return mark_safe(markdown.markdown(value, extensions=extensions))


@register.filter
def sub(value, arg):
    """ 빼기 필터 """
    return value-arg
