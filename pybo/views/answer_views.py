import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from pybo.forms import AnswerForm
from pybo.models import Question, Answer


@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    logging.info('answer_vote 함수')
    answer = get_object_or_404(Answer, id=answer_id)

    if answer.author == request.user:
        messages.error(request, "자기 자신을 추천 할 수 없습니다.")
    else:
        answer.voter.add(request.user)
    return redirect('pybo:detail', question_id=answer.question.pk)


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
            # http://127.0.0.1:8000/pybo/500/#answer_46
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question.id), answer.pk))

    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

