from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.views import generic
import logging
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

#def question_list(request):
    #questions = Question.objects.order_by('-create_date')
    #context = { 'questions' : questions }
    #return render (request, 'question_list.html', context)

#def question_view(request, question_id):
    #question = get_object_or_404(Question, pk=question_id)
    #context = {'question': question}
    #return render(request, 'question_view.html', context)


class QuestionListView(generic.ListView):
    paginate_by = 5
    model = Question
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger = logging.getLogger('test')
        logger.error(context)
        return context
    def get_queryset(self):
        return Question.objects.all().order_by('-create_date')

#class QuestionListView(generic.ListView):
   # paginate_by = 5
   # def get_queryset(self):
      #  context = Question.objects.all().order_by('-create_date')
      #  logger = logging.getLogger('test')
       # logger.error(context)
       # return context


class QuestionDetailView(generic.DetailView):
    model = Question

from django.utils import timezone

@login_required(login_url='common:login')
def answer_create(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('shop:detail', pk=pk)

from .forms import QuestionForm

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('shop:list')
    else:
        form = QuestionForm()
    context = {'form' : form}
    return render(request, 'shop/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('shop:detail', pk=question_id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form, 'question_id' : question.id}
    return render(request, 'shop/question_edit.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect('shop:list')