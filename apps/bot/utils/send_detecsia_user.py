from apps.user.models import Detecsia
from apps.bot.models import AllCar
from asgiref.sync import sync_to_async
from django.db.models import Q




async def get_user_active_cars(user):
    active_detecsias = await sync_to_async(list)(
        Detecsia.objects.filter(user=user, is_active=True)
    )

    query = Q()

    for detecsia in active_detecsias:
        query |= Q(carbrand=detecsia.car_brand, carmodel=detecsia.car_model)

    if query:
        matching_cars = await sync_to_async(list)(AllCar.objects.filter(query))
    else:
        matching_cars = []

    return matching_cars[:5]

