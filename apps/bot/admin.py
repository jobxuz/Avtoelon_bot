from django.contrib import admin

from apps.bot.models import TelegramBotConfiguration, CarBrand, CarModel, AllCar

# Register your models here.

admin.site.register(TelegramBotConfiguration)
admin.site.register(CarBrand)
admin.site.register(CarModel)
admin.site.register(AllCar)
