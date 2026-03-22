from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



tapalka = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Tap again", callback_data="tap_tap")],
    [InlineKeyboardButton(text="Ungrade tap", callback_data="upgrade_tap")],
    [InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])

tapalka_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Tap-tap", callback_data="tap_tap")],
    [InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])



builder_feed = InlineKeyboardBuilder()
builder_bath = InlineKeyboardBuilder()

builder_bath_again = InlineKeyboardBuilder()
builder_feed_again = InlineKeyboardBuilder()

builder_feed.button(text = "feed", callback_data="feed")
builder_bath.button(text = "bath", callback_data="bath")
builder_bath_again.button(text = "bath again", callback_data="bath")
builder_feed_again.button(text = "feed again", callback_data="feed")

feed_keyboard = builder_feed.as_markup()
bath_keyboard = builder_bath.as_markup()


bath_again_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Bath again", callback_data="bath")],
    [InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])
pet_again_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Pet again", callback_data="pet")],
    [InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])
feed_again_keyboard = builder_feed_again.as_markup()

menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Stats", callback_data="stats"), 
     InlineKeyboardButton(text="Care", callback_data="care"),
     InlineKeyboardButton(text="Shop", callback_data="shop")],

    [InlineKeyboardButton(text="Tap-tap", callback_data="tap_tap"), 
     InlineKeyboardButton(text="Bank", callback_data="bank"), 
     InlineKeyboardButton(text="Casino", callback_data="casino")]
])

menu_redirect = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])

go_to_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Go to menu", callback_data="menu")],
    [InlineKeyboardButton(text="Guide", callback_data="help")]
])

go_to_menu_lt = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Go to menu", callback_data="menu")]
])


taking_care = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Feed", callback_data="feed"),
     InlineKeyboardButton(text="Bath", callback_data="bath"),
     InlineKeyboardButton(text="Pet", callback_data="pet")],
    [InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])

nofood_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Shop", callback_data="shop")],
    [InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])

shop_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Food", callback_data="food")],
    [InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])

back_shop_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Back to shop", callback_data="shop")],
    [InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])

casino_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Lottery", callback_data="lottery"), 
     InlineKeyboardButton(text="Paper-Scissors-Rock", callback_data="psr"),
     InlineKeyboardButton(text="Number guess", callback_data="guess")],
    [InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])

lottery_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Buy a ticket", callback_data="ticket")],
    [InlineKeyboardButton(text="Back to casino", callback_data="casino"),
     InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])

again_lottery_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Buy a another ticket", callback_data="ticket")],
    [InlineKeyboardButton(text="Back to casino", callback_data="casino"),
     InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])

guess_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Play game", callback_data="guess_play")],
    [InlineKeyboardButton(text="Back to casino", callback_data="casino"),
     InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])

casino_back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Back to casino", callback_data="casino"),
     InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])

again_guess_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Play again", callback_data="guess_play")],
    [InlineKeyboardButton(text="Back to casino", callback_data="casino"),
     InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])

psr_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Play game", callback_data="psr_play")],
    [InlineKeyboardButton(text="Back to casino", callback_data="casino"),
     InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])

again_psr_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Play game again", callback_data="psr_play")],
    [InlineKeyboardButton(text="Back to casino", callback_data="casino"),
     InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])

bank_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Deposit", callback_data="deposit"),
     InlineKeyboardButton(text="Withdraw", callback_data="withdraw")],
    [InlineKeyboardButton(text="Back to the menu", callback_data="menu")]
])

back_bank_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Back to bank", callback_data="bank")],
    [InlineKeyboardButton(text="Back to menu", callback_data="menu")]
])