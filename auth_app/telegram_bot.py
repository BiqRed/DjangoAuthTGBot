import logging

from django.conf import settings
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from .models import LoginToken, TelegramUser

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) != 1:
            await update.message.reply_text("Неверный формат команды. Используйте /start <token>")
            return

        token_str = args[0]
        try:
            token = LoginToken.objects.get(token=token_str, used=False)
        except LoginToken.DoesNotExist:
            await update.message.reply_text("Неверный или использованный токен.")
            return

        # Получение или создание пользователя
        user = token.user

        # Создание или обновление TelegramUser
        telegram_id = str(update.effective_user.id)
        username = update.effective_user.username or update.effective_user.full_name

        TelegramUser.objects.update_or_create(
            telegram_id=telegram_id,
            defaults={
                'user': user,
                'username': username
            }
        )

        # Пометка токена как использованного
        token.used = True
        token.save()

        # Аутентификация пользователя (опционально можно отправить сообщение)
        await update.message.reply_text(f"Авторизация успешна! Вы можете закрыть это окно и вернуться на сайт.")

    except Exception as e:
        logger.error(f"Error in /start command: {e}")
        await update.message.reply_text("Произошла ошибка при авторизации.")


def run_bot():
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))

    # Запуск бота в режиме webhook
    application.run_polling()
