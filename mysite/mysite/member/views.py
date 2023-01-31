from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Member
from django.http import HttpResponse

# Create your views here.

def register(request) :
    if request.method == 'GET' :
        return render(request, 'register.html')
    elif request.method == 'POST' :
        username = request.POST.get('username', None)
        userid = request.POST.get('userid', None)
        userpass = request.POST.get('userpass', None)
        re_password = request.POST.get('re_password', None)
        email = request.POST.get('email', None)
        res_data = {}
        if not (username and userid and userpass and re_password and email):
            res_data['error'] = '모든 값을 입력하세요!'
            return render(request, 'register.html', res_data)
        elif userpass != re_password :
            res_data['error'] = '비밀번호가 다릅니다.'
            return render(request, 'register.html', res_data)
        else :
            member = Member(userid = userid, username = username, userpass = make_password(userpass), email = email)
            member.save()
        return redirect("/member/login")

from .forms import LoginForm

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form' : form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.userid
            return redirect('/')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form' : form})
"""
            userid = request.POST.get('userid', None)
            userpass = request.POST.get('userpass', None)
            res_data = {}
            if not (userid and userpass):
                res_data['error'] = '모든 값을 입력하세요!'
                return render(request, 'login.html', res_data)
            else :
                member = Member.objects.get(userid = userid)
                if check_password(userpass, member.userpass) :
                    request.session['user'] = member.id
                    return redirect('/')
                else :
                    res_data['error'] = '비밀번호가 다릅니다!'
"""

def home(request):
    user_id = request.session.get('user')
    if user_id :
        member = Member.objects.get(userid=user_id)
        return HttpResponse("환영합니다."+member.username+"님 <br> <a href='/member/logout'>로그아웃 </a>")
    else :
        return HttpResponse("Home!!!! <a href='/member/login'>로그인 </a>")

def logout(request) :
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('/')
