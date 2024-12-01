from django.contrib import admin
from .models import TelegramUser, LoginToken

admin.site.register(TelegramUser)
admin.site.register(LoginToken)
