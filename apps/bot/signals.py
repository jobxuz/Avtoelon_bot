import requests
from django.dispatch import receiver
from django.db.models.signals import pre_save

from apps.bot.models import TelegramBotConfiguration


@receiver(pre_save, sender=TelegramBotConfiguration)
def update_bot_webhook_url(sender, instance, **kwargs):
    try:
        existing_object = sender.objects.get(pk=instance.pk)
        if existing_object.webhook_url != instance.webhook_url:
            telegram_webhook_url = f'https://api.telegram.org/bot{instance.bot_token}/setWebhook?url={instance.webhook_url}'
            return requests.get(url=telegram_webhook_url)
    except TelegramBotConfiguration.DoesNotExist:
        pass
