from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.


def Registration(request):
    USFO=Userform()
    PFO=Profileform()
    D={'USFO':USFO,'PFO':PFO}
    if request.method=='POST' and request.FILES:
        UFDO=Userform(request.POST)
        PFDO=Profileform(request.POST,request.FILES)
        if UFDO.is_valid() and PFDO.is_valid():
            MUFDO=UFDO.save(commit=False)
            MUFDO.set_password(UFDO.cleaned_data['password'])
            MUFDO.save()

            MPFDO=PFDO.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()

            send_mail('registration','hello','vonaldios@gmail.com',[MUFDO.email],fail_silently=False)
            return render(request,'user_login.html')
        else:
            return HttpResponse('invalid data')
    return render(request,'Registration.html',D)

def welcome(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'welcome.html',d)
    return render(request,'welcome.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('welcome'))
        else:
            return HttpResponse('invalid credential')
    return render(request,'user_login.html')
    

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('welcome'))

@login_required
def display_profile(request):
    un=request.session.get('username')
    uo=User.objects.get(username=un)
    po=Profile.objects.get(username=uo)
    d={'uo':uo,'po':po}
    return render(request,'display_profile.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        uo=User.objects.get(username=request.session.get('username'))
        uo.set_password(pw)
        uo.save()

        return HttpResponse('password is changed successfully')
    return render(request,'change_password.html')

# @login_required
# def change_username(request):
#     if request.method=='POST':
#         un=request.POST['un']
#         uo=User.objects.get(username=request.session.get('username'))
#         uo.set_username(un)
#         uo.save()

#         return HttpResponse('password is changed successfully')
#     return render(request,'change_password.html')

def forget_password(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']

        LU=User.objects.filter(username=un)
        if LU:
            l=LU[0]
            l.set_password(pw)
            l.save()
            return HttpResponse('password set successfully')
        return HttpResponse('user not available')
    return render(request,'forget_password.html')