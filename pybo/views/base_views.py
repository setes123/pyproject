from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from ..models import Question


def index(request):
    # 모든 질문을 가져옴
    questions = Question.objects.all()  # 모든 Question 객체를 가져옵니다.

    # 페이징 처리: 한 페이지에 10개씩
    paginator = Paginator(questions, 10)  # 10개씩 나누기

    # 현재 페이지 번호를 가져옴 (URL의 'page' 파라미터)
    page_number = request.GET.get('page')  # URL에서 'page' 값을 가져옵니다.

    # 해당 페이지에 맞는 질문들을 가져옵니다.
    page_obj = paginator.get_page(page_number)  # 페이지에 해당하는 질문들

    # 페이지 템플릿에 질문들을 넘겨줍니다.
    return render(request, 'pybo/question_list.html', {'page_obj': page_obj})


def detail(request, question_id):
    # 질문 ID에 해당하는 질문을 가져옵니다. (없으면 404 에러)
    question = get_object_or_404(Question, pk=question_id)  # question_id로 질문을 찾습니다.

    # 해당 질문을 'question_detail.html' 템플릿으로 전달
    return render(request, 'pybo/question_detail.html', {'question': question})