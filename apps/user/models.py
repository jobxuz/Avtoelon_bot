from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _



class CustomUser(AbstractUser):
    tg_id = models.CharField(max_length=13, unique=True , verbose_name=_("Telegram Id"))
    phone_number = models.CharField(max_length=15, unique=True, verbose_name=_("Phone Number"))
    language = models.CharField(max_length=10, default="en", verbose_name=_("Language"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    last_active_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Last Active At"))


    def __str__(self):
        return self.first_name




class Detecsia(models.Model):
    car_brand = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.car_brand} ({'Active' if self.is_active else 'Inactive'})"
    






