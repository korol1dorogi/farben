from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import datetime
from .models import Seller, Client
User = get_user_model()  # Используем кастомную модель пользователя

def auth(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Проверяем существование пользователя с таким email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        # Если пользователь найден, проверяем пароль
        if user is not None and user.check_password(password):
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'auth.html', {'error': "Неверные почта или пароль"})

    return render(request, 'auth.html')

@login_required
def home(request):
    if request.method =='POST':
        try:
            with open('tes.txt','a') as a:
                a.write(request.POST.get('inn'))
                a.write(request.POST.get('amount'))
            with open('tes.txt','a') as a:
                a.write('дошел до формирования письма')
            subject = f'{Seller.objects.get(id=request.user.id)}'
            message = f'''
            Детали перевода:
            ИНН и ФИО покупателя: {Client.objects.get(inn=request.POST.get('inn'))}
            Передаваемая сумма: {request.POST.get('amount')} руб.
            Деньги принял: {Seller.objects.get(id=request.user.id)}
            Дата: {datetime.now().strftime("%d-%m-%Y %H:%M")}
            '''
            with open('tes.txt','a') as a:
                a.write('1о')
            from_email = settings.DEFAULT_FROM_EMAIL  # Используем настройки из settings.py
            recipient_list = [
                'avanesyan_dmitry@mail.ru',  # Ваш email для уведомлений
                'avanesyan_dmitry@mail.ru'  # Email клиента (если нужно)
                ]
            with open('tes.txt','a') as a:
                a.write('дошел от отправки')
    # Отправка письма
            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    recipient_list,
                    fail_silently=False
                )
            except Exception as e:
                print(f"Ошибка отправки: {str(e)}")
    
            messages.success(request, "Успешная отправка!")
            return redirect('home')
        except:
            messages.error(request, "Ошибка отправки")
            return redirect('home')

        
    return render(request, 'test.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('auth')


from django.http import JsonResponse
from .models import Client

@require_GET
@login_required
def check_inn(request):
    inn = request.GET.get('inn', '')
    try:
        client = Client.objects.get(inn=inn)
        return JsonResponse({
            'exists': True,
            'fio': client.full_name  # Используем свойство модели
        })
    except Client.DoesNotExist:
        return JsonResponse({'exists': False})
    
