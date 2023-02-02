from django.utils import timezone

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect

from pybo.models import Question, Answer
from pybo.forms import QuestionForm, AnswerForm
import logging


# Create your views here.
# def boot_menu(request):
#     return render()


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
            answer.save()  # 최종 저장
            return redirect('pybo:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed("Post만 가능 합니다.")

    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


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
            question.save()  # 날짜까지 생성해서 저장 (commit)
            return redirect("pybo:detail", question_id=question.id)
    else:
        form = QuestionForm()
    return render(request, 'pybo/question_form.html', {'form': form})


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

    context = {'question': question}
    return render(request, "pybo/question_detail.html", context)


def index(request):
    """ Question 목록 """
    logging.info("index 레벨로 출력")
    # list order create_date
    # Question.objects.order_by('create_date')  # ASC
    question_list = Question.objects.order_by('-create_date')  # DESC order_by('-필드')

    context = {'question_list': question_list}
    return render(request, "pybo/question_list.html", context)


