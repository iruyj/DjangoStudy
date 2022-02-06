from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse

from pybo.forms import QuestionForm, AnswerForm
from pybo.models import Question, Answer


def index(request):
    """
    pybo 목록 출력
    """
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list' : question_list}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """
        pybo 내용 출력
    """
    question = get_object_or_404(Question, pk =(question_id))
    context = {'question':question}
    return render(request, 'pybo/question_detail.html',context)
# Create your views here.

def answer_create(request, question_id):
    """
        pybo 답변등록
    """
    # request.POST.get('content') : form에 입력한텍스트를 포스트형태로 주었기때문에 request매개변수를 이용해서 다시 볼수있다.
    question = get_object_or_404(Question, pk=question_id)
    answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    answer.save()
    return redirect('pybo:detail', question_id= question.id)

def question_create(request):
    """
        pybo 질문 등록
    """
    # 동일한 URL 요청을 post, get 요청방식에 따라 다르게 처리
    # 1. GET
    # 질문 등록하기 버튼을 클릭한 경우 get방식으로 요청되어 question_create 함수 실행
        # 왜냐면 method를 지정하지않으면 무조건 GET 방식이기때문
    # 따라서 이경우에는 등록화면을 보여준다.
    # 2. POST
    # 질문등록 화면에서 post로 저장하기 버튼을 누르면 다음 코드들이 실행된다.
        # 1. GET과 다르게 form을 QuestionForm(request.POST)로 인수를 넣어서 생성했다.
            # 인수를 넣으면 request로 돌려받은 Post 데이터속에 담긴 subject,
            # content값이 QuestionForm의 subject, content 속성에 자동으로 저장되어 객체 생성됨
        # 2. form.is_valid()는 form이 유효한지를 검사한다. 만약 form에 저장된 subject, content의 값이 올바르지 않다면 form에는 오류
            # 메시지가 저장되고 form.is_valid()가 실패하여 다시 질문 등록 화면으로 돌아갈 것이다.
            #  이 때 form에 저장된 오류 메시지는 질문 등록 화면에 표시된다.
        # 3. 유효할경우
            # QuestionForm이 Question 모델과 연결된 모델 폼이기 때문에 즉시 저장할수있다.
            # question = form.save(commit=False) : 임시저장(아직값을 안넣었기때문에 save()할수없음
            # date를 따로 넣어준다. -> save() 저장
        # 4. return redirect('pybo:index') : 질문 목록 화면으로 이동
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form':form}
    return render(request, 'pybo/question_forms.html',context) # 폼 전달하기

def answer_create(request,question_id):
    '''
        pybo 답변등록
    '''
    question = get_object_or_404(Question, pk=question_id)
    if request.method =='POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail',question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question':question, 'form':form}
    return render(request, 'pybo/question_detail.html',context)