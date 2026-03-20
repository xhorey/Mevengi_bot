from aiogram import F, Router, html, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.functions import save_data, load_data, time_updates, find_price
from app.classes import TapUpgrade
from keyboards import tapalka, tapalka_back



#REST OF STUFF

router_tap = Router()

#!!! TAP-TAP !!!

@router_tap.callback_query(F.data == "tap_tap")
async def tap_money(callback: types.CallbackQuery):
    chat_id = str(callback.message.chat.id)
    mevengi_data = load_data()


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

    await callback.message.edit_text(f"You tapped and earned ${earning}🤑 \nYour balance now is 💵: ${mevengi_data[chat_id]['money']}.\nCurrent level of tap-tap: {mevengi_data[chat_id]['tap_tap_lvl']}.", reply_markup=tapalka)

    save_data(mevengi_data)


@router_tap.callback_query(F.data == "upgrade_tap")
async def tap_money(callback: types.CallbackQuery, state: FSMContext):
    chat_id = str(callback.message.chat.id)
    await time_updates(callback.message, False, True)
    mevengi_data = load_data() 

    if mevengi_data[chat_id]['tap_tap_lvl'] == 5:
        await callback.message.edit_text("You already have highest possible tap_tap level!", reply_markup=tapalka_back)
        return

    price_upgrade = find_price(callback.message)

    if int(mevengi_data[chat_id]['money']) < price_upgrade:
         await callback.message.edit_text(f"Upgrade costs ${price_upgrade}. You have not enough money!", reply_markup=tapalka_back)
         return
    
    await callback.message.edit_text(f"Upgrade costs ${price_upgrade}. Want to purchase?(type Yes for purchase and No for declining)")
    
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

        await message.answer(f"🆙You have upgraded tap_tap!🆙\nNew level is: {mevengi_data[chat_id]['tap_tap_lvl']}.", reply_markup=tapalka_back)
        save_data(mevengi_data)
        await state.clear()
        
        return
    
    if message.text.lower() == 'no':

        await message.answer(f"Ok. You exited upgrading menu. Use /help if needed.", reply_markup=tapalka_back)
        save_data(mevengi_data)
        await state.clear()
        
        return
    

    else:
         await message.answer("Please enter a valid answer 'Yes' or 'No'...")
