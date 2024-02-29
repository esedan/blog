from django.shortcuts import render, redirect
from account.models import User, Newsletters
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
from django.core.mail import send_mail
from random import randrange

# Create your views here.
def register(request):
    if request.method=="POST":
        user = request.POST.get('user')
        first= request.POST.get('first')
        last= request.POST.get('last')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        email1=request.POST.get('email1')
        email2=request.POST.get('email2')
        tel=request.POST.get('tel')

        if User.objects.filter(username=user).exists():
            messages.error(request, 'username already taken')
            return redirect('Register')
        
        if User.objects.filter(mobile=tel).exists():
            messages.error(request, 'phone number already taken')
            return redirect('Register')
        
        if email1 != email2:
            messages.error(request, 'check your email')
            return redirect('Register')

        if User.objects.filter(email=email2).exists():
            messages.error(request, 'email already taken')
            return redirect('Register')

        if pass1 != pass2:
            messages.error(request, 'check your password')
            return redirect('Register')

        user = User.objects.create_user(user, email2, pass1)
        user.first_name = first
        user.last_name= last
        user.mobile=tel
        user.save()
        messages.success(request, 'user created')
        return redirect('home')

    return render(request, 'account/register.html')

def logInUser(request):
    if request.method== 'POST':
        username=request.POST.get('user')
        pass1 = request.POST.get('pass1')

        user = authenticate(username=username, password= pass1)

        if user is not None:
            login(request,user)
        
        else:
            messages.error(request, 'invalid user')
            return redirect('login')

        messages.success(request, 'login successfull')
        return redirect('home')

    return render(request, 'account/log-in.html')

def logOut(request):
    logout(request)
    messages.success(request, 'logout successful')
    return redirect('login')

def forgotPassword(request):
    if request.method== 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email)
        user_email= User.objects.get(email=email)
        print('error')
        if user.exists():
            str_code = str(randrange(0,999999))
            code = str_code.zfill(8)

            subject= 'reset password'
            message = str(code)
            email_from =settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [user_email.email], fail_silently=False)

            user.update(forget_password_code=code)
            messages.success(request, 'the code has been sent to your email')
            return redirect('code', user_email.ref)

        else:
            messages.error(request, 'an error occurred')
            return redirect('login')
    return render(request, 'account/forgot password.html')

def code(request, ref):
    if request.method=='POST':
        user= User.objects.get(ref=ref)
        user_code= request.POST.get('code')
        if user_code == user.forget_password_code:
            messages.success(request, 'correct code')
            return redirect ('newpassword', user.ref)

        else:
            messages.error(request, 'incorrect code')
            return redirect('code', ref)
    return render(request, 'account/code.html')

def newPassword(request, ref):
    if request.method== 'POST':
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        user = User.objects.get(ref=ref)

        if pass1 == pass2 :
            user.set_password(pass2)
            user.forget_password_code= None
            user.save()
            messages.success(request, 'reset successful')
            return redirect('home')
        
        else:
            messages.error(request, 'incorrect password')
            return redirect('newpassword', ref)
        
    return render(request, 'account/new password.html')

@login_required(login_url='login')
def profile(request):
    # get cureent user info
    user = request.user
    # get  user info from database
    username = user.username
    email = user.email
    mobile = user.mobile
    first = user.first_name
    last = user.last_name
    picture = user.passport
    # password = user.pasword

    if request.method=="POST":
        # getting info from the input
        username = request.POST.get('user')
        email = request.POST.get('email')
        lastname = request.POST.get('last')
        firstname = request.POST.get('first')
        mobile = request.POST.get('mobile')
        picture = request.FILES['img']
        password = request.POST.get('password')
        # for validation 
        if not username or not email or not password:
            messages.error(request, 'All Fields are required')
            return redirect('profile')

        if username != user.username and User.objects.filter(username=username).exists():
            messages.error(request,'Username alrady Taken')
            return redirect('profile')
        
        if email != user.email and User.objects.filter(email=email).exists():
            messages.error(request,'email alrady Taken')
            return redirect('profile')
            
            # update and save to database
        user.username = username
        user.email = email
        user.set_password(password)
        user.last_name = lastname
        user.first_name = firstname
        user.mobile = mobile
        user.passport = picture
        user.save()
        messages.success(request, 'Profile Updated Successfully')
        return redirect('home')

    data={
        'username': username,
        'email' : email,
        # 'password': password,
        'lastname': last,
        'firstname': first,
        'mobile': mobile,
        'picture': picture
    }

    return render(request, 'account/profile form.html', data )

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        Newsletters.objects.create(email=email)
    return redirect('home')

def sendNewsLetter(request):
    if request.method=='POST':
        receiver= []
        mails= Newsletters.objects.filter(status= True)
        for mail in mails:
            receiver.append(mail.email)
        
        subject= request.POST.get('subject')
        message= request.POST.get('message')
        email_from= settings.EMAIL_HOST_USER
        send_email(subject, message, email_from, receiver, fail_silently= False)
        messages.success(request, 'Sent')
        return redirect('newsletter')
    return render(request, 'account/newsletter.html')