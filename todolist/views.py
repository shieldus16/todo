from django.forms import ValidationError
from django.shortcuts import render, redirect
from .models import User,Todo
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect
from .models import User
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.serializers import serialize
from django.http import HttpResponse

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
        
        # 성공 시 세션에 사용자 아이디 저장
        request.session['user_id'] = user.user_id
        print(request.session['user_id'])
        
        return redirect('calendar')  # 성공 페이지
    
    return render(request, 'todolist/login.html')

def logout(request):
    # 세션에서 사용자 아이디 삭제
    if 'user_id' in request.session:
          del(request.session['user_id'])
    return redirect('calendar') 

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
        
        # 비밀번호 DB 저장 전 해싱
        hashed_password = make_password(password)
        # 사용자 생성 및 랜덤 색상 할당
        new_user = User(user_id=id, user_password=password, user_name=name)
        new_user.user_color = generate_random_color()
        new_user.save()
        
        return redirect('login')
    
    return render(request, 'todolist/signup.html')
    

def generate_random_color():
    existing_colors = User.objects.values_list('user_color', flat=True)
    while True:
        # 랜덤한 색상을 #RRGGBB 형식으로 생성
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

        # 생성한 색상이 이미 존재하는지 확인
        if color not in existing_colors:
            return color

@api_view(['GET'])
def get_todo(request):
    date = request.query_params.get('date', None)
    print('Processed date:', date)
    if date:
        # 받아온 날짜를 이용하여 Todo 필터링
        todos = Todo.objects.filter(todo_date=date)
        todos_serialized = serialize('json', todos)
    
        return HttpResponse(todos_serialized, content_type='application/json')
    else:
        # 날짜가 전달되지 않은 경우 에러 응답 반환
        return HttpResponse('Date parameter is required.', status=400)
