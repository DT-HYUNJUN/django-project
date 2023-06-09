from django.shortcuts import render, redirect
from .forms import CustomUserChangeForm, CustomUserCreationForm, CustomPasswordChangeForm, CustomAuthenticationForm, CustomUserImageForm
from .models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.


# 로그인
def login(request):
    if request.user.is_authenticated:
        return redirect('posts:index')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            if request.POST.get('next'):
                url = request.POST.get('next')
            else:
                url = 'posts:index'
            return redirect(url)
        else:
            print('login failed')
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


# 로그아웃
@login_required
def logout(request):
    auth_logout(request)
    return redirect('posts:index')


# 회원 가입
def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('posts:index') 
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


# 회원 정보 변경
@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('posts:profile')
    else:
        form = CustomUserChangeForm(instance= request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


# 회원 탈퇴
@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('posts:index')


# 비밀번호 변경
@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('posts:index')
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)


# 프로필
@login_required
def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    form = CustomUserChangeForm()
    context = {
        'person': person,
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def image_upload(request, user_pk):
    form = CustomUserImageForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('accounts:profile')


@login_required
def image_delete(request, user_pk):
    user = User.objects.get(pk=user_pk)
    user.image = None
    user.save()
    return redirect('accounts:profile')


def follow(request, user_pk):
    User = get_user_model()
    you = User.objects.get(pk=user_pk)
    me = request.user
    if you != me:
        if you.followers.filter(pk=me.pk).exists():
            you.followers.remove(me)
            IS_FOLLOWED = False
        else:
            you.followers.add(me)
            IS_FOLLOWED = True
        context = {
            'is_followed': IS_FOLLOWED,
            'followings_count': you.followings.count(),
            'followers_count': you.followers.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:profile', you.username)