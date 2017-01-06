from django.shortcuts import render,get_object_or_404
from django.core import serializers
from django.http import Http404,JsonResponse,HttpResponse
from .models import Question
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import QuestionCreateForm
# Create your views here.

@csrf_exempt
def all_questions(request):

   # context={'name':'Yogesh','phone':7838451168}
    context={'q_list':Question.objects.all()}
    return render(request,'question/index.html',context);

# django require http methods to check method
'''
@require_GET
def show_question_add_form(request):
    return render(request,'question/create_form.html')


@require_POST
def save_question(request):
    title=request.POST.get('title','')
    if not title:
        raise Http404
    q=Question.objects.create(title=title,created_by=request.user)
    #print(request.POST)
    return HttpResponse('ok')

@require_GET
@csrf_exempt
def get_question(request,id=None):
    if request.method!='GET':
        raise Http404
    if not id:
        raise Http404;
    
        #q=Question.objects.get(id=id)
    q=get_object_or_404(Question,id=id)
    #get returns only one so it raises an exception
    #data ={'id':q.id,'title':q.title,'text':q.text}
    #return JsonResponse(data);
    data=serializers.serialize('json',[q]);
    return HttpResponse(data, content_type="application/json");
'''
@require_http_methods(['GET','POST'])
@login_required
def add_question(request):
    if request.method=='GET':
        #f=QuestionCreateForm(initial={'title':'Hey'})
        f=QuestionCreateForm()
    else:
        f=QuestionCreateForm(request.POST)
        if f.is_valid():
            question_obj=f.save(commit=False)
            question_obj.created_by=request.user
            question_obj.save()
            return HttpResponse('ok')
    return render(request,'question/add.html',{'f':f})

@require_http_methods(['GET','POST'])
@login_required
def edit_question(request,id=None):
    question_obj=get_object_or_404(Question,id=id)
    if question_obj.created_by!=request.user:
        raise Http404()
    if request.method=='GET':
        f=QuestionCreateForm(instance=question_obj)
    else:
        f=QuestionCreateForm(request.POST,instance=question_obj)
        if f.is_valid():
            question_obj=f.save()
            return HttpResponse('ok')
    context={'f':f,'q_id':question_obj.id}
    return render(request,'question/edit.html',context)

