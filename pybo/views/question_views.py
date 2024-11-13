from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


# 질문 생성 뷰
@login_required(login_url='common:login')  # 로그인하지 않으면 로그인 페이지로 리다이렉트
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)  # 전달된 데이터로 폼 인스턴스를 생성
        if form.is_valid():
            question = form.save(commit=False)  # 유효한 폼이면 데이터를 저장하지만 아직 DB에 저장하지 않음
            question.author = request.user  # 현재 로그인한 사용자로 질문 작성자 설정
            question.create_date = timezone.now()  # 질문 작성 시간을 현재 시간으로 설정
            question.save()  # 질문을 DB에 저장
            messages.success(request, '질문이 등록되었습니다.')  # 성공 메시지 표시
            return redirect('pybo:question_list')  # 질문 목록 페이지로 리다이렉트
    else:
        form = QuestionForm()  # GET 요청이면 빈 폼을 전달
    return render(request, 'pybo/question_form.html', {'form': form})  # 질문 폼 템플릿 렌더링


# 질문 수정 뷰
@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)  # 주어진 ID에 해당하는 질문을 가져옴
    if question.author != request.user:  # 로그인한 사용자와 질문 작성자가 다르면 수정 불가
        messages.error(request, '권한이 없습니다.')
        return redirect('pybo:question_detail', question_id=question.id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)  # 기존 질문 데이터로 폼 인스턴스를 생성
        if form.is_valid():
            form.save()  # 수정된 데이터를 저장
            messages.success(request, '질문이 수정되었습니다.')  # 성공 메시지
            return redirect('pybo:question_detail', question_id=question.id)  # 수정된 질문 상세 페이지로 리다이렉트
    else:
        form = QuestionForm(instance=question)  # GET 요청이면 기존 질문 데이터로 폼을 생성
    return render(request, 'pybo/question_form.html', {'form': form})  # 질문 수정 폼 렌더링


# 질문 삭제 뷰
@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)  # 주어진 ID에 해당하는 질문을 가져옴
    if question.author != request.user:  # 로그인한 사용자와 질문 작성자가 다르면 삭제 불가
        messages.error(request, '권한이 없습니다.')
        return redirect('pybo:question_detail', question_id=question.id)

    question.delete()  # 질문 삭제
    messages.success(request, '질문이 삭제되었습니다.')  # 삭제 성공 메시지
    return redirect('pybo:question_list')  # 질문 목록 페이지로 리다이렉트
