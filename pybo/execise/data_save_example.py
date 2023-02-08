"""
파일명 : data_save_example.py
설 명 : 
생성일 : 2023-01-26
생성자 : hamin
since 2023.01.09 Copyright (C) by Hamin All right reserved.
"""

from django.utils import timezone
from pybo.models import Question, Answer

# q = Question(subject="파이썬 게시판은 무엇인가요?", content='알고 싶어요!', create_date=timezone.now())
q = Question(subject="장고 모델은 무엇인가요?", content='알고 싶어요!', create_date=timezone.now())
q.save()

# 데이터 모두 추출
Question.objects.all()

# 필터로 추출
Question.objects.filter(id=2)

# 데이터 수정
q = Question.objects.get(id=2)

q.subject = 'Django Model은 무엇인가요?'
q.save()

q = Question.objects.get(id=1)
a = Answer(question=q, content='id는 자동 생성 됩니다.', create_date=timezone.now())
a.save()

a = Answer.objects.get(id=1)
a.question

q.answer_set.all()
