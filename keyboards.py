from aiogram.utils.keyboard import InlineKeyboardBuilder

builder = InlineKeyboardBuilder()

builder.button(text="tap-tap", callback_data="tap_tap")

tapalka = builder.as_markup()