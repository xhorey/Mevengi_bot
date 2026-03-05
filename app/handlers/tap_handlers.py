from aiogram import F, Router, html
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.functions import save_data, load_data, time_updates, find_price
from app.classes import TapUpgrade



#REST OF STUFF

router_tap = Router()

#!!! TAP-TAP !!!


@router_tap.message(Command('tap_tap'))
async def show_stats(message: Message):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()

    if chat_id not in mevengi_data:
        await message.answer("Seems like you have no mevengis yet. Use /create to create one!")
        return
    if mevengi_data[chat_id]['tap_tap_lvl'] == 1:
        money = int(mevengi_data[chat_id]['money']) + 5
        earning = 5
    elif mevengi_data[chat_id]['tap_tap_lvl'] == 2:
        money = int(mevengi_data[chat_id]['money']) + 10
        earning = 10
    elif mevengi_data[chat_id]['tap_tap_lvl'] == 3:
        money = int(mevengi_data[chat_id]['money']) + 15
        earning = 15
    elif mevengi_data[chat_id]['tap_tap_lvl'] == 4:
        money = int(mevengi_data[chat_id]['money']) + 20
        earning = 20
    else:
        money = int(mevengi_data[chat_id]['money']) + 50
        earning = 50
    mevengi_data[chat_id]['money'] = str(money)
    await message.answer(f"You tapped and earned ${earning}! Your balance now is ${mevengi_data[chat_id]['money']}.\nCurrent level of tap-tap: {mevengi_data[chat_id]['tap_tap_lvl']}. To upgrade it use /upgrade_tap.")

    save_data(mevengi_data)


@router_tap.message(Command('upgrade_tap'))
async def upgrade_tap_tap(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()  
    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await time_updates(message, False, True)

    mevengi_data = load_data() 

    if mevengi_data[chat_id]['tap_tap_lvl'] == 5:
        await message.answer("You already have highest possible tap_tap level!")
        return

    price_upgrade = find_price(message)

    if int(mevengi_data[chat_id]['money']) < price_upgrade:
         await message.answer(f"Upgrade costs ${price_upgrade}. You have not enough money!")
         return
    
    await message.answer(f"Upgrade costs ${price_upgrade}. Want to purchase?(type Yes for purchase and No for declining)")
    
    await state.set_state(TapUpgrade.choice)
    
    save_data(mevengi_data)

@router_tap.message(TapUpgrade.choice)
async def upgrade_tap_tap(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    
    await time_updates(message, False, True)

    mevengi_data = load_data() 

    if message.text.lower() == 'yes':

        price_upgrade = find_price(message)

        new_money = int(mevengi_data[chat_id]['money']) - price_upgrade

        mevengi_data[chat_id]['money'] = str(new_money)

        mevengi_data[chat_id]['tap_tap_lvl'] += 1

        await message.answer(f"You have upgraded tap_tap! New level is: {mevengi_data[chat_id]['tap_tap_lvl']}.")
        save_data(mevengi_data)
        await state.clear()
        
        return
    
    if message.text.lower() == 'no':

        await message.answer(f"Ok. You exited upgrading menu. Use /help if needed.")
        save_data(mevengi_data)
        await state.clear()
        
        return
    

    else:
         await message.answer("Please enter a valid answer 'Yes' or 'No'...")
