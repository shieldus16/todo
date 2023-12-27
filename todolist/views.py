from django.forms import ValidationError
from django.shortcuts import render, redirect
from .models import User,Todo
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError



def calendar(request):
    return render(request, 'todolist/calendar.html')

@csrf_protect
def login(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(user_id=id, user_password=password)
        except User.DoesNotExist:
            return render(request, 'todolist/login.html', {'error_message': '아이디 또는 비밀번호가 올바르지 않습니다.'})
        return redirect('calendar')  # 성공 페이지
        
    return render(request, 'todolist/login.html')

@csrf_protect
def signup(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        password = request.POST.get('password')
        name = request.POST.get('name')
        # 아이디 중복 확인
        try:
            user = User.objects.get(user_id=id)
            return render(request, 'todolist/signup.html', {'error_message': '이미 존재하는 아이디입니다.'})
        except User.DoesNotExist:
            pass  # 아이디가 존재하지 않으면 계속 진행
        
        # 비밀번호 검증
        try:
            validate_password(password)
        except ValidationError as e:
            return render(request, 'todolist/signup.html', {'error_message': str(e)})
        try:
            user = User.objects.get(user_id=id, user_password=password)
        except User.DoesNotExist:
            new_user = User(user_id=id, user_password=password, user_name=name)
            new_user.save()
            return redirect('login')
    
    return render(request, 'todolist/signup.html')
