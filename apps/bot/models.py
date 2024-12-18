from django.db import models
from solo.models import SingletonModel
from apps.user.models import Detecsia

# Create your models here.

class TelegramBotConfiguration(SingletonModel):
    bot_token = models.CharField(max_length=255, default='token')
    secret_key = models.CharField(max_length=255, default='secret_key')
    webhook_url = models.URLField(max_length=255, default='https://api.telegram.org/')
    admin = models.IntegerField(default=1235678)




class CarBrand(models.Model):
    name = models.CharField(max_length=50,unique=True)


    def __str__(self):
        return self.name
    


class CarModel(models.Model):
    brend = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.name




class AllCar(models.Model):
    carbrand = models.CharField(max_length=256, null=True, blank=True)
    carmodel = models.CharField(max_length=256, null=True, blank=True)
    images_str = models.TextField(null=True, blank=True)
    full_title = models.CharField(max_length=256, null=True, blank=True)
    price_text = models.CharField(max_length=256, null=True, blank=True)
    description_params_str = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=256, null=True, blank=True)
    description_text = models.TextField(null=True, blank=True)
    main_url = models.CharField(max_length=256, null=True, blank=True)
    data_id = models.CharField(max_length=256, null=True, blank=True)
    detecsia = models.ForeignKey(Detecsia, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.full_title
    
