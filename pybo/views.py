from django.utils import timezone

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from pybo.models import Question, Answer


# Create your views here.
def boot_menu(request):
    return render()


def answer_create(request, question_id):
    print("answer_create question_id:{}".format(question_id))
    question = get_object_or_404(Question, pk=question_id)

    question.answer_set.create(content=request.POST.get("content"), create_date=timezone.now())

    return redirect('pybo:detail', question_id=question.id)


def register(request):
    return render(request, "pybo/question_register.html")


def detail(request, question_id):
    """Question 상세"""
    print(question_id)
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)

    context = {'question': question}
    return render(request, "pybo/question_detail.html", context)


def index(request):
    """ Question 목록 """

    # list order create_date
    # Question.objects.order_by('create_date')  # ASC
    question_list = Question.objects.order_by('-create_date')  # DESC order_by('-필드')

    context = {'question_list': question_list}
    return render(request, "pybo/question_list.html", context)


