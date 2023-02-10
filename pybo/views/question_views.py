import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from pybo.forms import QuestionForm
from pybo.models import Question


@login_required(login_url='common:login')
def vote_question(request, question_id):
    logging.info('request.method : {}'.format(request.method))
    question = get_object_or_404(Question, id=question_id)

    # 본인 글은 본인이 추천 하지 못하게
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천 할 수 없습니다.')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)


@login_required(login_url='common:login')  # 로그인이 되어있지 않으면 login 페이지로 이동
def register(request):
    """ 질문 등록 """

    logging.info('request.method : {}'.format(request.method))
    form = None
    if request.method == "POST":
        logging.info("question_create post")
        # 저장
        form = QuestionForm(request.POST)  # request.POST 데이터 (그냥 request는 GET이 default)
        if form.is_valid():  # form(질문 등록)이 유용하면
            question = form.save(commit=False)  # subject와 content만 저장 (DB에 물리적으로 commit은 하지 않음)
            question.create_date = timezone.now()
            question.author = request.user  # author 속성에 로그인 계정 저장
            logging.info('4. question.author: {}'.format(question.author))

            question.save()  # 날짜까지 생성해서 저장 (commit)
            return redirect("pybo:detail", question_id=question.id)
    else:
        form = QuestionForm()
    context = {'form': form, 'url': "{% url 'pybo:register' %}"}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def modify_question(request, question_id):
    logging.info("request.method: {}".format(request.method))
    context = None
    question = get_object_or_404(Question, id=question_id)
    if request.user.username != question.author.username:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()

            question.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question)
        context = {'form': form, 'url': ""}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def delete_question(request, question_id):
    logging.info("request.method: {}".format(request.method))
    question = get_object_or_404(Question, pk=question_id)

    if request.user.username != question.author.username:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)

    question.delete()
    return redirect('index')

# def question_create(request):
#     question = Question(subject=request.POST.get("subject"),
#                         content=request.POST.get("content"),
#                         create_date=timezone.now())
#     question.save()
#     return redirect('pybo:detail', question_id=question.id)


def detail(request, question_id):
    """Question 상세"""
    logging.info(question_id)
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        question.views += 1
        question.save()

    context = {'question': question, 'user': request.user}
    return render(request, "pybo/question_detail.html", context)
