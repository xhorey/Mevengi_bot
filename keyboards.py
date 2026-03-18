from aiogram.utils.keyboard import InlineKeyboardBuilder

builder_tapalka = InlineKeyboardBuilder()

builder_tapalka.button(text="tap-tap", callback_data="tap_tap")

tapalka = builder_tapalka.as_markup()





builder_feed = InlineKeyboardBuilder()
builder_bath = InlineKeyboardBuilder()

builder_feed.button(text = "feed", callback_data="feed")
builder_bath.button(text = "bath", callback_data="bath")

feed_keyboard = builder_feed.as_markup()
bath_keyboard = builder_bath.as_markup()
