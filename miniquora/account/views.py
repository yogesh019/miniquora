from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse, HttpResponse
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout  
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm,ForgotPassword,SetPassword,SignupForm
from .models import MyUser,create_otp,get_valid_otp_object
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template import loader
# Create your views here.

#@required_login set a get parameter next in the url

def hello(request):
    print(request)
    print(request.GET.get('abc',''))
    
    return HttpResponse('<h1>Hello</h1>')
'''
@require_GET
def show_login(request):
    if request.user.is_authenticated():
        return redirect(reverse('home',kwargs={'id':user.id}));
    return render(request,'account/auth/login.html');

'''
@require_http_methods(['GET','POST'])
def login(request):
    if request.user.is_authenticated():
        return redirect(reverse('home',kwargs={'id':request.user.id}));
    if request.method=='GET':
        context={'f':LoginForm()};
        return render(request,'account/auth/login.html',context);
    else:
        f=LoginForm(request.POST);
        if not f.is_valid():
            return render(request,'account/auth/login.html',{'f':f});
        else:
            #user=MyUser.objects.get(username=f.cleaned_data.get('username'))
            #user=authenticate(username=f.cleaned_data['username'],password=f.cleaned_data['password'])
            #user.backend='django.contrib.auth.backends.ModelBackend'
            #print(user.backend)
            auth_login(request,f.authenticated_user);
            return redirect(reverse('home',kwargs={'id':f.authenticated_user.id}));
    

def forgot_password(request):
    if request.user.is_authenticated():
        return redirect(reverse('home',kwargs={'id':request.user.id}));
    if request.method=='GET':
        context={'f':ForgotPassword()};
        return render(request,'account/auth/forgot_password.html',context);
    else:
        f=ForgotPassword(request.POST)
        if not f.is_valid():
            return render(request,'account/auth/forgot_password.html',{'f':f});
        else:
            user=MyUser.objects.get(username=f.cleaned_data['username'])
            otp=create_otp(user=user,purpose='FP')
            #send email
            email_body_context={'u':user,'otp':otp}
            body=loader.render_to_string('account/auth/email/forgot_password.txt',email_body_context)
            message=EmailMultiAlternatives("Reset Password",body,settings.EMAIL_HOST_USER,[user.email])
            #message.attach_alternative(html_body,'text/html')
            message.send()
            return render(request,'account/auth/forgot_email_sent.html',{'u':user})



def reset_password(request,id=None,otp=None):
    if request.user.is_authenticated():
        return redirect(reverse('home',kwargs={'id':request.user.id}));
    user=get_object_or_404(MyUser,id=id)
    otp_object=get_valid_otp_object(user=user,purpose='FP',otp=otp)
    if not otp_object:
        raise Http404();
    if request.method=='GET':
        f=SetPassword()
        context={'f':f,'otp':otp_object.otp,'uid':user.id}
        return render(request,'account/auth/set_password.html',context)
    else:
        f=SetPassword(request.POST)
        if f.is_valid():
            user.set_password(f.cleaned_data['new_password'])
            user.save()
            otp_object.delete()
            return render(request,'account/auth/set_password_success.html',{'u':user})
        context={'f':f,'otp':otp_object.otp,'uid':user.id}
        return render(request,'account/auth/set_password.html',context)

    
@require_GET
@login_required
def home(request,id):
    #if not request.user.is_authenticated():
     #   return redirect(reverse('base'))
    return render(request,'account/auth/loggedin.html')

def logout(request):
    auth_logout(request)
    return redirect(reverse('login'));


def signup(request):
    if request.user.is_authenticated():
        return redirect(reverse('home',kwargs={'id':request.user.id}));
    if request.method=='GET':
        context={'f':SignupForm()};
        return render(request,'account/auth/signup.html',context);
    else:
        f=SignupForm(request.POST)
        if not f.is_valid():
            return render(request,'account/auth/signup.html',{'f':f});
        else:
            user=f.save(commit=False)
            user.set_password(f.cleaned_data['password'])
            user.is_active=False
            user.save()
            
            #user=MyUser.objects.get(username=f.cleaned_data['username'])
            otp=create_otp(user=user,purpose='AA')
            #send email
            email_body_context={'u':user,'otp':otp}
            body=loader.render_to_string('account/auth/email/activation_link.txt',email_body_context)

            message=EmailMultiAlternatives("Activation Link",body,settings.EMAIL_HOST_USER,[user.email])
            #message.attach_alternative(html_body,'text/html')
            message.send()
            return render(request,'account/auth/activation_link_sent.html',{'u':user})

''' Activate Account'''
@require_GET
def activate(request,id=None,otp=None):
    user=get_object_or_404(MyUser,id=id)
    otp_object=get_valid_otp_object(user=user,purpose='AA',otp=otp)
    if not otp_object:
        raise Http404();
    user.is_active=True
    user.save()
    otp_object.delete()
    return render(request,'account/auth/activation_successful.html',{'u':user})


