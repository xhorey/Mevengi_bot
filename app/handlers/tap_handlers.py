from aiogram import F, Router, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import json
import random
import time

from app.classes import Mevengi, Creation, NameChange, NumberGuess, PaperScissorsRock, TapUpgrade, Banking






     

#!!! PRICE !!!

def find_price(message:Message):
     mevengi_data = load_data()
     chat_id = str(message.chat.id)
     if mevengi_data[chat_id]['tap_tap_lvl'] == 1:
          return 200
     if mevengi_data[chat_id]['tap_tap_lvl'] == 2:
          return 500
     if mevengi_data[chat_id]['tap_tap_lvl'] == 3:
          return 2500
     if mevengi_data[chat_id]['tap_tap_lvl'] == 4:
          return 5000
     




#DATA FUNCTIONS


def load_data():
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)



#!!! SATIETY AND HYGIENE UPDATE !!!

async def update_satiety_and_hygiene(message: Message, is_bathing):
     mevengi_data = load_data()
     chat_id = str(message.chat.id)
     now = time.time()
     two_minutes_passed = (now - mevengi_data[chat_id]['last_update']) / 120
     decrease_satiety = two_minutes_passed
     decrease_hygiene = two_minutes_passed/2
     mevengi_data[chat_id]['satiety'] -= decrease_satiety
     mevengi_data[chat_id]['hygiene_number'] -= decrease_hygiene

     if mevengi_data[chat_id]['satiety'] < 0:
          mevengi_data[chat_id]['satiety'] = 0

     if mevengi_data[chat_id]['hygiene_number'] < 0:
          mevengi_data[chat_id]['hygiene_number'] = 0

     if int(mevengi_data[chat_id]['satiety']) < 30:
        await message.answer("Your Mevengi is hungry  and gets sad...")
        if mevengi_data[chat_id]['happiness']>0:
            mevengi_data[chat_id]['happiness'] -= 5

     if 80 <= mevengi_data[chat_id]['hygiene_number'] <= 100:
          mevengi_data[chat_id]['hygiene_status'] = 'Perfectly clean'
     elif 60 <= mevengi_data[chat_id]['hygiene_number'] < 80:
          mevengi_data[chat_id]['hygiene_status'] = 'Good'
     elif 40 <= mevengi_data[chat_id]['hygiene_number'] < 60:
          mevengi_data[chat_id]['hygiene_status'] = 'A bit sweaty'
     elif 20 <= mevengi_data[chat_id]['hygiene_number'] < 40:
          mevengi_data[chat_id]['hygiene_status'] = 'Stinks'
          if is_bathing == False:
               await message.answer("Your Mevengi stinks! It's better to give it some bath as soon as possible!")
     else:
          mevengi_data[chat_id]['hygiene_status'] = 'Horrible'
          if is_bathing == False:
               await message.answer("Your Mevengi stinks so bad! Give it some bath NOW!!!")


     mevengi_data[chat_id]['last_update'] = now
     
     
     save_data(mevengi_data)

#REST OF STUFF

router_tap = Router()

file_path = "app/data.json"

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
    
    await update_satiety_and_hygiene(message, False)

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
    
    await update_satiety_and_hygiene(message, False)

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
