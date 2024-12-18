import requests
from django.dispatch import receiver
from django.db.models.signals import pre_save

from apps.bot.models import TelegramBotConfiguration

from django.db.models.signals import post_migrate
from .models import CarBrand
from .utils.bs4data import get_car_brands
from django.db.models.signals import post_save

from apps.user.models import CustomUser


@receiver(pre_save, sender=TelegramBotConfiguration)
def update_bot_webhook_url(sender, instance, **kwargs):
    try:
        existing_object = sender.objects.get(pk=instance.pk)
        if existing_object.webhook_url != instance.webhook_url:
            telegram_webhook_url = f'https://api.telegram.org/bot{instance.bot_token}/setWebhook?url={instance.webhook_url}'
            return requests.get(url=telegram_webhook_url)
    except TelegramBotConfiguration.DoesNotExist:
        pass






@receiver(post_save, sender=CustomUser)
def user_created_signal(sender, instance, created, **kwargs):
    if created: 
        print(f"Yangi foydalanuvchi qo'shildi: {instance}")
        if not CarBrand.objects.exists(): 
            car_brands = get_car_brands()  
            if car_brands:
                for brand in car_brands:
                    CarBrand.objects.create(name=brand)
                print("CarBrand modeliga brendlar qo'shildi.")
            else:
                print("Brendlar ro'yxatini olishda muammo yuz berdi.")
        




