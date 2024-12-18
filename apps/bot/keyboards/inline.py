from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async
from math import ceil
from apps.bot.models import CarBrand, CarModel




# @sync_to_async
# def get_car_brands():
#     return CarBrand.objects.all()

# @sync_to_async
# def get_car_models():
#     return CarModel.objects.all()




language_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🇺🇿 uz',callback_data='uz'),
            InlineKeyboardButton(text='🇺🇸 eng',callback_data='en'),
            InlineKeyboardButton(text='🇷🇺 ru',callback_data='ru')
        ],
    ]
)



mainmenu_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Yangi detektsiya yaratish',callback_data='new_detection'),
            InlineKeyboardButton(text='Faol detektsiyalar',callback_data="activedetections")
        ],
        [
            InlineKeyboardButton(text='Sozlamalar',callback_data='settings')
        ],
    ]
)


detecsi_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Detektsiya yaratish',callback_data='createdetecsia'),
            InlineKeyboardButton(text="Filtr qo‘shish",callback_data="carfilter")
        ],
        [
            InlineKeyboardButton(text='Ortga',callback_data='backdetecsia')
        ],
    ]
)




# def create_car_brands_key(car_brands):
#     inline_keyboard = InlineKeyboardBuilder()
#     for brand in car_brands:
#         inline_keyboard.button(
#             text=brand.name,
#             callback_data=f"{brand.name}"
#         )

#     inline_keyboard.adjust(2)
#     return inline_keyboard.as_markup()


def create_car_brands_key(car_brands, page=1, page_size=10):
    inline_keyboard = InlineKeyboardBuilder()

    # Pagination hisoblash
    total_pages = ceil(len(car_brands) / page_size)
    start = (page - 1) * page_size
    end = start + page_size
    current_page_items = car_brands[start:end]

    # Car brand tugmalarini qo'shish
    for brand in current_page_items:
        inline_keyboard.button(
            text=brand.name,
            callback_data=f"{brand.name}"  # Brendni aniqlash uchun callback_data
        )

    # Sahifa tugmalarini qo‘shish
    if page > 1:
        inline_keyboard.button(
            text="⬅️ Oldingi",
            callback_data=f"page:{page - 1}"  # Oldingi sahifa uchun callback
        )
    if page < total_pages:
        inline_keyboard.button(
            text="Keyingi ➡️",
            callback_data=f"page:{page + 1}"  # Keyingi sahifa uchun callback
        )

    inline_keyboard.adjust(2)  # Har bir qatorda 2 ta tugma
    return inline_keyboard.as_markup()






# def create_car_models_key(car_models):
#     inline_keyboard = InlineKeyboardBuilder()

#     for model in car_models:
#         inline_keyboard.button(
#             text=model.name,
#             callback_data=f"{model.name.lower()}" 
#         )

#     inline_keyboard.adjust(2)
#     return inline_keyboard.as_markup()



def create_car_models_key(car_models, page=1, page_size=10):
    inline_keyboard = InlineKeyboardBuilder()

    # Pagination hisoblash
    total_pages = ceil(len(car_models) / page_size)
    start = (page - 1) * page_size
    end = start + page_size
    current_page_items = car_models[start:end]

    # Model tugmalarini qo'shish
    for model in current_page_items:
        inline_keyboard.button(
            text=model.name,
            callback_data=f"{model.name.lower()}"  # Callback uchun model nomi
        )

    # Sahifa tugmalarini qo‘shish
    if page > 1:
        inline_keyboard.button(
            text="⬅️ Oldingi",
            callback_data=f"model_page:{page - 1}"
        )
    if page < total_pages:
        inline_keyboard.button(
            text="Keyingi ➡️",
            callback_data=f"model_page:{page + 1}"
        )

    inline_keyboard.adjust(2)  # Har bir qatorda 2 ta tugma
    return inline_keyboard.as_markup()




def detecsia_key(detecsias):
    inline_keyboard = InlineKeyboardBuilder()

    for detecsia in detecsias:
        inline_keyboard.button(
            text=f"{detecsia.car_brand}|{detecsia.car_model} | {'✅' if detecsia.is_active else '❌'}",
            callback_data=f"{detecsia.car_brand}_{detecsia.car_model}" 
        )

    inline_keyboard.adjust(1)
    return inline_keyboard.as_markup()




detecsia_update_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Faollashtirish/Faolsizlantirish',callback_data='detecsia_update'),
            InlineKeyboardButton(text='Filtrlarni o‘zgartirish',callback_data='update_filter')
            
        ],
        [
            InlineKeyboardButton(text='Detektsiyani o‘chirish',callback_data='delete_detecsia'),
            InlineKeyboardButton(text='Hisobot',callback_data='hisobot')
        ],
        [
            InlineKeyboardButton(text='Bosh sahifa',callback_data='boshsahifa')
        ]
    ]
)