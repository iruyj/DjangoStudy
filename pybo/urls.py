from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'),
    path('pybo/<int:question_id>/', views.detail, name ='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    #   '' 로 경로 설정한 이유 : 위에 urls에서 pybo/을 설정해서 합쳐져 결국 pybo/가 됨
    path('question/create/',views.question_create, name='question_create'),
]