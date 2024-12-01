from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import LoginToken, TelegramUser


def home(request):
    if request.user.is_authenticated:
        try:
            telegram_user = TelegramUser.objects.get(user=request.user)
            context = {
                'telegram_username': telegram_user.username
            }
        except TelegramUser.DoesNotExist:
            context = {}
    else:
        context = {}
    return render(request, 'home.html', context)


@login_required
def login_with_telegram(request):
    if request.user.is_authenticated:
        # Генерация уникального токена
        token = LoginToken.objects.create(user=request.user)

        # Ссылка на бота с токеном
        bot_username = 'YOUR_BOT_USERNAME'  # Замените на имя вашего бота без @
        telegram_link = f"https://t.me/{bot_username}?start={token.token}"

        context = {
            'telegram_link': telegram_link
        }

        return render(request, 'login_with_telegram.html', context)
    else:
        return redirect('login')
