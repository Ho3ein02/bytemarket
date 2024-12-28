from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import PhoneForm, UserInfoForm
from random import choices
import time


def verify_phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if phone:
                # Generate a random 6 digit code
                code = ''.join(choices([str(i) for i in range(9)], k=6))
                # The code is valid for 2 minutes
                code_time = time.time() + 120
                token_code = {
                    'code': code,
                    'code_time': code_time,
                }
                # Add the phone and the code and its time expire, to the session
                request.session['phone'] = phone
                request.session['token_code'] = token_code
                return redirect('account:verify_code')
    else:
        form = PhoneForm()
    return render(request, 'account/login.html', {'form': form})


def verify_code(request):
    if request.method == 'POST':
        # Get the code that the user entered
        code = request.POST.get('verify_code')
        # Get the code and its time expire in the session
        token_code = request.session.get('token_code')
        
        # Check the correctness of the code entered by the user and the expiration time of the code
        if code == token_code['code'] and time.time() < token_code['code_time']:
            # Get the user phone number from the session
            phone = request.session.get('phone')
            user = authenticate(request, phone=phone)
            # If user does not exists, create a new user with that phone number
            if not user:
                user = User.objects.create_user(phone=phone)
            del request.session['phone']
            del request.session['token_code']
            
            # If the user was redirected to the login page, than take its url to return to the target page
            next_url = request.session.get('next_url')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Check that the user was redirected to the login page
            if next_url:
                return redirect(next_url)
            return redirect('shop:index')
        else:
            messages.error(request, 'کد نا معتبر است.')
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
        return redirect('account:verify_code')


def user_logout(request):
    logout(request)
    return redirect('shop:index')


@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'account/profile.html', context)


@login_required
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

