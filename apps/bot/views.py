import json
from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from aiogram import Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from apps.bot.config.bot import dp
from apps.bot.models import TelegramBotConfiguration


# Create your views here.
class TelegramWebhook(View):
    @method_decorator(csrf_exempt)  # Отключает CSRF-проверку для метода post
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    async def post(self, request):
        # telegram_conf = TelegramBotConfiguration.get_solo()
        bot = Bot(token='BOT_TOKEN', default=DefaultBotProperties(parse_mode=ParseMode.HTML))

        try:
            data = json.loads(request.body)
            print(data)  # Логируем данные для отладки
            await dp.feed_update(bot=bot, update=types.Update(**data))
        except json.JSONDecodeError:
            print('error')
            return HttpResponse("Invalid JSON", status=400)

        # Здесь обработка данных из Telegram Webhook
        return HttpResponse('Webhook updated successfully')
