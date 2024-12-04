from aiogram.utils.keyboard import InlineKeyboardBuilder
from apps.bot.utils.db_manager import db
from apps.bot.utils.callback_data import cb_main_menu_callback_data, MainMenuAction, cb_back_to_main_menu_callback_data, \
    cb_select_language_callback_data, SelectLanguage, BranchCallbackData, \
    CategoryCallbackData, back_to_food_menu_callback_data, \
    BackToFoodMenuAction, ProductItemOrderCallbackData, ProductOrderCallbackData

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_back_to_main_menu():
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.button(text='Asosiy menu',
                           callback_data=cb_back_to_main_menu_callback_data())
    return inline_keyboard.as_markup()


def inline_main_menu():
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.button(text='🏠️️ Buyurtma berish',
                           callback_data=cb_main_menu_callback_data(action=MainMenuAction.ORDER))
    inline_keyboard.button(text='Biz haqimizda', callback_data=cb_main_menu_callback_data(action=MainMenuAction.ABOUT))
    inline_keyboard.button(text='Buyurtmalarim',
                           callback_data=cb_main_menu_callback_data(action=MainMenuAction.MY_ORDERS))
    inline_keyboard.button(text='Filiallar', callback_data=cb_main_menu_callback_data(action=MainMenuAction.BRANCHES))
    inline_keyboard.button(text='Sozlamalar', callback_data=cb_main_menu_callback_data(action=MainMenuAction.SETTINGS))

    inline_keyboard.adjust(2)

    return inline_keyboard.as_markup()


def inline_subscribe():
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.button(text='Subscribe', url='https://t.me/oqtepalavashuz')

    return inline_keyboard.as_markup()


def inline_languages():
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.button(text='Uzbek', callback_data=cb_select_language_callback_data(lang=SelectLanguage.UZ))
    inline_keyboard.button(text='Russian', callback_data=cb_select_language_callback_data(lang=SelectLanguage.RU))
    inline_keyboard.button(text='English', callback_data=cb_select_language_callback_data(lang=SelectLanguage.EN))

    inline_keyboard.adjust(1)

    return inline_keyboard.as_markup()


async def inline_branches():
    inline_keyboard = InlineKeyboardBuilder()
    branches = await db.fetch("SELECT branch_id, name FROM branches")
    for branch in branches:
        inline_keyboard.button(
            text=branch['name'],
            callback_data=BranchCallbackData(branch_id=branch['branch_id']).pack()
        )
    inline_keyboard.button(text='Asosiy menu',
                           callback_data=cb_back_to_main_menu_callback_data())
    inline_keyboard.adjust(2)
    return inline_keyboard.as_markup()


async def inline_categories(categories):
    inline_keyboard = InlineKeyboardBuilder()
    for category in categories:
        inline_keyboard.button(
            text=category['name'],
            callback_data=CategoryCallbackData(category_id=category['category_id']).pack()
        )
    inline_keyboard.button(text='Ortga',
                           callback_data=back_to_food_menu_callback_data(action=BackToFoodMenuAction.BACK))
    inline_keyboard.adjust(2)

    return inline_keyboard.as_markup()


async def inline_product_catalog(products: list):
    inline_keyboard = InlineKeyboardBuilder()
    for product in products:
        inline_keyboard.button(
            text=product['name'],
            callback_data=ProductOrderCallbackData(product_id=product['product_id']).pack()
        )
    inline_keyboard.button(text="Ortga",
                           callback_data=back_to_food_menu_callback_data(action=BackToFoodMenuAction.BACK))

    inline_keyboard.adjust(2)
    return inline_keyboard.as_markup()


def inline_settings():
    inline_keyboard = InlineKeyboardBuilder()

    inline_keyboard.button(text="Muloqot tili", callback_data='settings')
    inline_keyboard.button(text="Telefon", callback_data='phone')
    inline_keyboard.button(text="Shahar", callback_data='city')
    inline_keyboard.button(text="Asosiy menu", callback_data=cb_back_to_main_menu_callback_data())
    inline_keyboard.adjust(3)

    return inline_keyboard.as_markup()


def inline_order_food_item_keyboard(product_id: int, quantity: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="-", callback_data=ProductItemOrderCallbackData(action="decrease",
                                                                                          product_id=product_id,
                                                                                          quantity=quantity).pack()),
                InlineKeyboardButton(text=f"{quantity}", callback_data="ignore"),
                InlineKeyboardButton(text="+", callback_data=ProductItemOrderCallbackData(action="increase",
                                                                                          product_id=product_id,
                                                                                          quantity=quantity).pack()),
            ],
            [
                InlineKeyboardButton(text="🛒 Add to Cart",
                                     callback_data=ProductItemOrderCallbackData(action="add_to_cart",
                                                                                product_id=product_id,
                                                                                quantity=quantity).pack())
            ],
            [
                InlineKeyboardButton(text="🔙 Back",
                                     callback_data=ProductItemOrderCallbackData(action="back", product_id=product_id,
                                                                                quantity=quantity).pack())
            ],
        ]
    )


def inline_nearest_branches(branches):
    inline_keyboard = InlineKeyboardBuilder()
    for branch in branches:
        inline_keyboard.button(
            text=branch['name'],
            callback_data=BranchCallbackData(branch_id=branch['branch_id']).pack()
        )
    inline_keyboard.adjust(1)
    return inline_keyboard.as_markup()
