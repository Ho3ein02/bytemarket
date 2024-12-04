from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import User
from .forms import PhoneForm, UserInfoForm
from random import choices
import time
from .password_generator import random_password_generator
from .sendSMS import send_login_code


def verify_phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if phone:
                code = ''.join(choices([str(i) for i in range(9)], k=6))
                code_time = time.time() + 120
                token_code = {
                    'code': code,
                    'code_time': code_time,
                }
                request.session['phone'] = phone
                request.session['token_code'] = token_code
                # send_login_code(phone, code=code)
                return redirect('account:verify_code')
    else:
        form = PhoneForm()
    return render(request, 'account/login.html', {'form': form})


def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('verify_code')
        token_code = request.session.get('token_code')
        if code == token_code['code'] and time.time() < token_code['code_time']:
            phone = request.session.get('phone')
            user = authenticate(request, phone=phone)
            if not user:
                random_password = random_password_generator()
                user = User.objects.create_user(phone=phone)
                user.set_password(random_password)
                user.save()
            del request.session['phone']
            del request.session['token_code']
            next_url = request.session.get('next_url')
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect('shop:index')
        else:
            messages.error(request, 'کد نا معتبر است.')
    else:
        code = request.session['token_code']['code']
    return render(request, 'account/verify_code.html', {'code': code})


def resend_code(request):
    phone = request.session.get('phone')
    if phone:
        code = ''.join(choices([str(i) for i in range(9)], k=6))
        code_time = time.time() + 120
        token_code = {
            'code': code,
            'code_time': code_time,
        }
        request.session['phone'] = phone
        request.session['token_code'] = token_code
        # send_login_code(phone, code=code)
        print(code)
        return redirect('account:verify_code')


def user_logout(request):
    logout(request)
    return redirect('shop:index')


@login_required
def profile(request):
    user = request.user
    form = UserInfoForm(instance=user)
    context = {
        'user': user,
        'form': form,
    }
    return render(request, 'account/profile.html', context)


def user_info_edit(request):
    user = request.user
    if request.method == 'POST':
        form = UserInfoForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
    else:
        form = UserInfoForm(instance=user)
    return render(request, 'account/user_info_edit.html', {'form': form})

