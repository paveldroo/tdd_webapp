import os
import sys
import uuid

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from accounts.models import Token


def send_login_email(request):
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print('saving uid', uid, 'for email', email, file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(
        subject='Your login link for Superlists',
        message=f'Use this link to log in:\n\n{url}',
        from_email=os.getenv('EMAIL_HOST_USER'),
        recipient_list=[email]
    )
    return render(request, 'login_email_sent.html')


def login(request):
    print('login view', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')
