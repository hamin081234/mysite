from django.utils import timezone
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect

from pybo.models import Question, Answer
from pybo.forms import QuestionForm, AnswerForm
import logging
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
# def boot_menu(request):
#     return render()

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    logging.info('answer_delete에 잘 들어왔다')

    answer = get_object_or_404(Answer, pk=answer_id)

    if answer.author.username != request.user.username:
        messages.error(request, "권한이 없습니다.")
        return redirect('pybo:detail', question_id=answer.question.pk)

    answer.delete()
    return redirect('pybo:detail', question_id=answer.question.pk)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    logging.info("answer_modify에 잘 들어왔다")

    answer = get_object_or_404(Answer, pk=answer_id)

    if answer.author.username != request.user.username:
        messages.error(request, "권한이 없습니다.")
        return redirect('pybo:detail', question_id=answer.question.pk)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()

            answer.save()
            return redirect('pybo:detail', question_id=answer.question.pk)

    form = AnswerForm(instance=answer)
    context = {'form': form, 'question': answer.question}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_create(request, question_id):
    logging.info("answer_create question_id:{}".format(question_id))
    question = get_object_or_404(Question, pk=question_id)

    form = AnswerForm()
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.author = request.user

            answer.save()  # 최종 저장
            return redirect('pybo:detail', question_id=question.id)

    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


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

    context = {'question': question, 'user': request.user}
    return render(request, "pybo/question_detail.html", context)


def index(request):
    """ Question 목록 """
    logging.info("index 레벨로 출력")
    # list order create_date
    # Question.objects.order_by('create_date')  # ASC

    #입력인자
    page = request.GET.get("page", '1')
    question_list = Question.objects.order_by('-create_date')  # DESC order_by('-필드')

    paginator = Paginator(question_list, 10)
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

    context = {'question_list': page_obj}
    logging.info('question_list:{}'.format(page_obj))

    return render(request, "pybo/question_list.html", context)


