from aiogram import F, Router, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import json
import random
import time

from app.classes import Mevengi, Creation, NameChange, NumberGuess, PaperScissorsRock, TapUpgrade, Banking






     





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

router_treatment = Router()

file_path = "app/data.json"

#!!! FEED !!!

@router_treatment.message(Command('feed'))
async def show_stats(message: Message):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()

    
    if chat_id not in mevengi_data:
        await message.answer("Seems like you have no mevengis yet. Use /create to create one!")
        return

    if mevengi_data[chat_id]['satiety'] >= 100:
        await message.answer("Your mevengi is not hungry!")
        return
        

    if int(mevengi_data[chat_id]['money']) >= 10:
        new_money = int(mevengi_data[chat_id]['money']) - 10
        mevengi_data[chat_id]['money'] = str(new_money)
        mevengi_data[chat_id]["satiety"] += 10
        await message.answer(
            f"You fed the Mevengi! 💖\n"
            f"Balance left: ${mevengi_data[chat_id]['money']}\n"
            f"Satiety: {int(mevengi_data[chat_id]['satiety'])}"
        )
        level_up = int(mevengi_data[chat_id]['level_up']) + 10
        
        if level_up >= 100:
            new_level = int(mevengi_data[chat_id]['level']) + 1
            mevengi_data[chat_id]['level'] = new_level
            level_up -= 100
            await message.answer(f"Your mevengi has grew up! Now it's lvl.{new_level}")
            if new_level == 2:
                mevengi_data[chat_id]['casino_locker'] = False
                await message.answer("You have unlocked casino now! Have fun!")
            if new_level == 5:
                mevengi_data[chat_id]['bank_locker'] = False
                await message.answer("You have unlocked bank now!") 

        mevengi_data[chat_id]['level_up'] = str(level_up)

        save_data(mevengi_data)
    else:
        await message.answer("Seems like you are too poor for this...")



#!!! PET !!!

@router_treatment.message(Command('pet'))
async def petting(message: Message):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()  
    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await update_satiety_and_hygiene(message, False)

    mevengi_data = load_data() 

    if mevengi_data[chat_id]['happiness'] < 100:
        mevengi_data[chat_id]['happiness'] += 2

    await message.answer(f"You pet your Mevengi <3\nHappiness: {mevengi_data[chat_id]['happiness']}", parse_mode=None)
    
    save_data(mevengi_data)




#!!! BATH !!!

@router_treatment.message(Command('bath'))
async def petting(message: Message):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()  
    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await update_satiety_and_hygiene(message, True)

    mevengi_data = load_data()

    mevengi_data[chat_id]['hygiene_number'] += 15
    save_data(mevengi_data)

    if mevengi_data[chat_id]['hygiene_number'] > 100:
       mevengi_data[chat_id]['hygiene_number'] = 100 

    if 80 <= mevengi_data[chat_id]['hygiene_number'] <= 100:
          mevengi_data[chat_id]['hygiene_status'] = 'Perfectly clean'
    elif 60 <= mevengi_data[chat_id]['hygiene_number'] < 80:
          mevengi_data[chat_id]['hygiene_status'] = 'Good'
    elif 40 <= mevengi_data[chat_id]['hygiene_number'] < 60:
          mevengi_data[chat_id]['hygiene_status'] = 'A bit sweaty'
    elif 20 <= mevengi_data[chat_id]['hygiene_number'] < 40:
          mevengi_data[chat_id]['hygiene_status'] = 'Stinks'
    else:
          mevengi_data[chat_id]['hygiene_status'] = 'Horrible'

    await message.answer(f"You washed your Mevengi! Now it's hygiene status is: {mevengi_data[chat_id]['hygiene_status']}.")
    

    save_data(mevengi_data)

