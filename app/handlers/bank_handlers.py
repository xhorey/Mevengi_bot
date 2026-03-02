from aiogram import F, Router, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import json
import random
import time

from app.classes import Mevengi, Creation, NameChange, NumberGuess, PaperScissorsRock, TapUpgrade, Banking


router_bank = Router()

file_path = "app/data.json"



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






@router_bank.message(Command('bank'))
async def bank_menu(message: Message):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()  
    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await update_satiety_and_hygiene(message, False)

    mevengi_data = load_data() 

    if mevengi_data[chat_id]['bank_locker']:
         await message.answer(f"This section unlocks on level 5!")
         save_data(mevengi_data)
         return

    await message.answer(f"Here is your bank account.\nUse /deposit to put money on your account and get some % every 5 hours. \nUse /withdraw to withdraw money from your deposit.")
    
    
    save_data(mevengi_data)


@router_bank.message(Command('deposit'))
async def deposit(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()  
    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await update_satiety_and_hygiene(message, False)

    mevengi_data = load_data() 

    if mevengi_data[chat_id]['bank_locker']:
         await message.answer(f"This section unlocks on level 5!")
         save_data(mevengi_data)
         return

    await message.answer(f"How much money you want to deposit? Enter the number.")
    await state.set_state(Banking.deposit)
    
    save_data(mevengi_data)

@router_bank.message(Banking.deposit)
async def deposit_second(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    
    await update_satiety_and_hygiene(message, False)

    mevengi_data = load_data() 

    if message.text.lower() == 'exit':
        await state.clear()
        await message.answer("You exited the deposit state! You can use /help if needed.")
        return
    
    if message.text.isdigit():
                deposit = int(message.text)
                if deposit <= int(mevengi_data[chat_id]['money']):
                    new_balance = int(mevengi_data[chat_id]['money']) - deposit
                    mevengi_data[chat_id]['bank_money'] += deposit
                    mevengi_data[chat_id]['money'] = str(new_balance)
                    save_data(mevengi_data)
                    await state.clear()
                    await message.answer(f"You deposited ${deposit}! Money on your account: ${mevengi_data[chat_id]['bank_money']}.")
                    
                else:
                    await message.answer(f"You are too poor for this big deposit. Current amount of money you have: ${mevengi_data[chat_id]['money']}.\nType-in 'exit' if u wanna exit depositing state or try lower amount.")
    else:
                await message.answer("Enter valid number.")
    
    
    save_data(mevengi_data)



@router_bank.message(Command('withdraw'))
async def upgrade_tap_tap(message: Message):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()  
    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await update_satiety_and_hygiene(message, False)

    mevengi_data = load_data() 

    if mevengi_data[chat_id]['bank_locker']:
         await message.answer(f"This section unlocks on level 5!")
         save_data(mevengi_data)
         return




    await message.answer(f"")
    
    
    save_data(mevengi_data)