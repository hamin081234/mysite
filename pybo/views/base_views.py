import logging

from django.core.paginator import Paginator
from django.shortcuts import render

from pybo.models import Question


def index(request):
    """ Question 목록 """
    logging.info("index 레벨로 출력")
    # list order create_date
    # Question.objects.order_by('create_date')  # ASC

    # 입력인자
    page = request.GET.get("page", '1')
    kw = request.GET.get("kw", '')
    s_type = request.GET.get("type", 'subject')
    rows = request.GET.get("rows", '10')
    logging.info("page:{}".format(page))
    logging.info("kw:{}".format(kw))

    question_list = Question.objects.order_by('-create_date')  # DESC order_by('-필드')
    # subject_container : 사용 __contains 또는 __icontains (대소 문자 구분)
    if s_type == "content":
        question_list = question_list.filter(content__contains=kw)
    elif s_type == "author":
        question_list = question_list.filter(author__username__contains=kw)
    else:
        question_list = question_list.filter(subject__contains=kw)

    paginator = Paginator(question_list, int(rows))
    page_obj = paginator.get_page(page)
    # paginator.count : 전체 개시물 개수
    # paginator.per_page : 페이지당 보여줄 게시물 개수
    # paginator.page_range : 페이지 범위
    # number: 현재 페이지 번호
    # previous_page_number: 이전 페이지 번호
    # next_page_number: 다음 페이지 번호
    # has_previous: 이전 페이지 유무
    # has_next: 다음 페이지 유무
    # start_index: 현재 페이지 시작 인덱스 (1부터 시작)
    # end_index: 현재 페이지 끝 인덱스

    context = {'question_list': page_obj, 'kw': kw, 'page': page, 'type': s_type, 'rows': int(rows)}
    logging.info('question_list:{}'.format(page_obj))

    return render(request, "pybo/question_list.html", context)

