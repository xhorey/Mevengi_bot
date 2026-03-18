from aiogram import F, Router, html
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import json
import time
import random

from app.classes import Banking
from keyboards import feed_keyboard, bath_keyboard



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

async def time_updates(message: Message, is_bathing, notify):
     mevengi_data = load_data()
     chat_id = str(message.chat.id)
     now = time.time()
     two_minutes_passed = (now - mevengi_data[chat_id]['last_update']) / 120
     decrease_satiety = two_minutes_passed
     decrease_hygiene = two_minutes_passed/2

     if mevengi_data[chat_id]['deposited']:
        deposit_count_hour = (now - mevengi_data[chat_id]['last_update']) / 3600
        mevengi_data[chat_id]['deposit_counter'] += deposit_count_hour
        if mevengi_data[chat_id]['deposit_counter'] >= 5:
             times = int(mevengi_data[chat_id]['deposit_counter'] // 5)
             for i in range(times):
                mevengi_data[chat_id]['deposit_counter'] -= 5
                mevengi_data[chat_id]['bank_money'] = mevengi_data[chat_id]['bank_money'] * 1.05
             
     
     mevengi_data[chat_id]['satiety'] -= decrease_satiety
     mevengi_data[chat_id]['hygiene_number'] -= decrease_hygiene

     if mevengi_data[chat_id]['satiety'] < 0:
          mevengi_data[chat_id]['satiety'] = 0

     if mevengi_data[chat_id]['hygiene_number'] < 0:
          mevengi_data[chat_id]['hygiene_number'] = 0

     if int(mevengi_data[chat_id]['satiety']) < 30:
        if notify:
          await message.answer("Your Mevengi is hungry  and gets sad 💔", reply_markup=feed_keyboard)
          if mevengi_data[chat_id]['happiness']>0:
               mevengi_data[chat_id]['happiness'] -= 5
               if mevengi_data[chat_id]['happiness']<0:
                    mevengi_data[chat_id]['happiness'] = 0

     if 80 <= mevengi_data[chat_id]['hygiene_number'] <= 100:
          mevengi_data[chat_id]['hygiene_status'] = 'Perfectly clean'
     elif 60 <= mevengi_data[chat_id]['hygiene_number'] < 80:
          mevengi_data[chat_id]['hygiene_status'] = 'Good'
     elif 40 <= mevengi_data[chat_id]['hygiene_number'] < 60:
          mevengi_data[chat_id]['hygiene_status'] = 'A bit sweaty'
     elif 20 <= mevengi_data[chat_id]['hygiene_number'] < 40:
          mevengi_data[chat_id]['hygiene_status'] = 'Stinks'
          if is_bathing == False:
               await message.answer("Your Mevengi stinks 🫢! It's better to give it some bath as soon as possible!", reply_markup=bath_keyboard)
     else:
          mevengi_data[chat_id]['hygiene_status'] = 'Horrible'
          if is_bathing == False:
               await message.answer("Your Mevengi stinks so bad 🤢! Give it some bath NOW!!!", reply_markup=bath_keyboard)


     mevengi_data[chat_id]['last_update'] = now
     
     
     save_data(mevengi_data)


#CASINO FUNCTIONS

def lottery_ticket():
     result_lottery = random.randint(1, 100000)
     if 0<result_lottery<=16:
          return "super_jackpot"
     elif 16<result_lottery<=216:
          return "jackpot"
     elif 216<result_lottery<=8216:
          return "win"
     else:
          return "lose"



def random_number_generator():
    number = random.randint(1, 10)
    if number < 5:
        return '2'   
    elif number == 5:
        return '3'  
    else:
        return '1'  
     


def choice_psr():
     number = random.randint(1,3)
     if number == 1:
          print("paper")
          return "paper"
     elif number == 2:
          print("scissors")
          return "scissors"
     elif number ==3:
          print("rock")
          return "rock"

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
     



#!!! INVENTORY !!!

def inventory_show(message: Message):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()  
    str_inventory = ""
    for i in mevengi_data[chat_id]['inventory']:
        str_inventory += str(i) + f" - {mevengi_data[chat_id]['inventory'][i]}\n"
    return str_inventory



#!!! EMOJI !!!
def get_emoji_state(message: Message):
     chat_id = str(message.chat.id)
     mevengi_data = load_data() 
     if 70 <= mevengi_data[chat_id]['happiness'] <= 100: 
          return "😁"
     elif 50 <= mevengi_data[chat_id]['happiness'] < 70:
          return "🙂"
     elif 30 <= mevengi_data[chat_id]['happiness'] < 50:
          return "😐"
     elif 10 <= mevengi_data[chat_id]['happiness'] < 30:
          return "😢"
     elif 0 <= mevengi_data[chat_id]['happiness'] < 10:
          return "😭"