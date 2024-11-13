from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer


# 답변 생성 뷰
@login_required(login_url='common:login')  # 로그인하지 않으면 로그인 페이지로 리다이렉트
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)  # 주어진 ID에 해당하는 질문을 가져옴

    if request.method == 'POST':
        form = AnswerForm(request.POST)  # 전달된 데이터로 폼 인스턴스를 생성
        if form.is_valid():
            answer = form.save(commit=False)  # 유효한 폼이면 답변 객체 생성
            answer.author = request.user  # 로그인한 사용자로 답변 작성자 설정
            answer.create_date = timezone.now()  # 답변 작성 시간을 현재 시간으로 설정
            answer.question = question  # 해당 질문에 대한 답변이므로 question 필드에 질문을 설정
            answer.save()  # 답변을 DB에 저장
            messages.success(request, '답변이 등록되었습니다.')  # 성공 메시지
            return redirect('pybo:question_detail', question_id=question.id)  # 해당 질문 상세 페이지로 리다이렉트
    else:
        form = AnswerForm()  # GET 요청이면 빈 폼을 전달
    return render(request, 'pybo/answer_form.html', {'form': form, 'question': question})  # 답변 폼 렌더링


# 답변 수정 뷰
@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)  # 주어진 ID에 해당하는 답변을 가져옴
    question = answer.question  # 해당 답변이 속한 질문을 가져옴

    if answer.author != request.user:  # 로그인한 사용자와 답변 작성자가 다르면 수정 불가
        messages.error(request, '권한이 없습니다.')
        return redirect('pybo:question_detail', question_id=question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)  # 기존 답변 데이터로 폼 인스턴스를 생성
        if form.is_valid():
            form.save()  # 수정된 데이터를 저장
            messages.success(request, '답변이 수정되었습니다.')  # 성공 메시지
            return redirect('pybo:question_detail', question_id=question.id)  # 해당 질문 상세 페이지로 리다이렉트
    else:
        form = AnswerForm(instance=answer)  # GET 요청이면 기존 답변 데이터로 폼을 생성
    return render(request, 'pybo/answer_form.html', {'form': form, 'question': question})  # 답변 수정 폼 렌더링


# 답변 삭제 뷰
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)  # 주어진 ID에 해당하는 답변을 가져옴
    question = answer.question  # 해당 답변이 속한 질문을 가져옴

    if answer.author != request.user:  # 로그인한 사용자와 답변 작성자가 다르면 삭제 불가
        messages.error(request, '권한이 없습니다.')
        return redirect('pybo:question_detail', question_id=question.id)

    answer.delete()  # 답변 삭제
    messages.success(request, '답변이 삭제되었습니다.')  # 삭제 성공 메시지
    return redirect('pybo:question_detail', question_id=question.id)  # 해당 질문 상세 페이지로 리다이렉트
