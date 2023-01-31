from django.urls import path
#from .views import question_list, question_view
from . import views
from .views import answer_create
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

app_name = 'shop'

urlpatterns = [
    #path("", question_list),
    #path("qna/<int:question_id>", question_view),
    path("", login_required(views.QuestionListView.as_view(), login_url='common:login'), name="list"),
    path("qna/<int:pk>", login_required(views.QuestionDetailView.as_view(), login_url='common:login'), name="detail"),
    path("answer/create/<int:pk>", views.answer_create, name="answer_create"),
    path("question/create", views.question_create, name="question_create"),
    path("question/modify/<int:question_id>", views.question_modify, name="question_modify"),
    path("question/delete/<int:question_id>", views.question_delete, name="question_delete"),
]