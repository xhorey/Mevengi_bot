from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

builder_tapalka = InlineKeyboardBuilder()

builder_tapalka.button(text="tap-tap", callback_data="tap_tap")

tapalka = builder_tapalka.as_markup()





builder_feed = InlineKeyboardBuilder()
builder_bath = InlineKeyboardBuilder()

builder_bath_again = InlineKeyboardBuilder()
builder_feed_again = InlineKeyboardBuilder()

builder_feed.button(text = "feed", callback_data="feed")
builder_bath.button(text = "bath", callback_data="bath")
builder_bath_again.button(text = "bath again", callback_data="bath_again")
builder_feed_again.button(text = "feed again", callback_data="feed_again")

feed_keyboard = builder_feed.as_markup()
bath_keyboard = builder_bath.as_markup()
bath_again_keyboard = builder_bath_again.as_markup()
feed_again_keyboard = builder_feed_again.as_markup()

menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Stats", callback_data="stats"), InlineKeyboardButton(text="Care", callback_data="care"),InlineKeyboardButton(text="Shop", callback_data="shop")],
    [InlineKeyboardButton(text="Tap-tap", callback_data="tap_tap"), InlineKeyboardButton(text="Bank", callback_data="bank"), InlineKeyboardButton(text="Casino", callback_data="casino")]
])
