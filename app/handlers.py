from aiogram import F, Router, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import json
import random
import time

from app.classes import Mevengi, Creation, NameChange, NumberGuess, PaperScissorsRock, TapUpgrade






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
     

#REST OF STUFF

router = Router()

file_path = "app/data.json"

  


#!!! CREATION !!!

@router.message(CommandStart())
async def command_start(message: Message):
    chat_id = str(message.chat.id)
    data = load_data()

    if chat_id in data:
        await message.answer("This chat already has a Mevengi.")
    else:
        await message.answer(
            f"Hello, {html.bold(message.from_user.full_name)}!\n"
            "Create a Mevengi for this chat using /create"
        )

@router.message(Command('create'))
async def command_create(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    data = load_data()
        
    if chat_id in data:
        await message.answer("Seems like you already have mevengi, use commands to interact with it =). For command list use /help if you need.")
    else:
        await state.set_state(Creation.name)
        await message.answer("Type in new Mevengi name")
    

@router.message(Creation.name)
async def command_create_second_stage(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    chat_id = str(message.chat.id)
    fsm_data = await state.get_data()

    mevengi = Mevengi(
        name=fsm_data["name"],
        mevengi_id=chat_id,
        last_update = time.time()
    )

    data = load_data()

    data[chat_id] = {
        "id": mevengi.id,
        "name": mevengi.name,
        "level": mevengi.level,
        "money": mevengi.money,
        "level_up": mevengi.level_up,
        "satiety": mevengi.satiety,
        "happiness": mevengi.happiness,
        "last_update": mevengi.last_update,
        "hygiene_status": 'Perfectly clean',
        "hygiene_number": 100,
        "casino_locker": True,
        "tap_tap_lvl": 1

    }

    save_data(data)

    await message.answer(
        f"Your new Mevengi:\n"
        f"Name: {mevengi.name}\n"
        f"Age: {mevengi.level}\n"
        f"Money: {mevengi.money}\n"
        f"Satiety: {mevengi.satiety}\n"
        f"Happiness: {mevengi.happiness}\nHygiene status: {data[chat_id]['hygiene_status']}\n\nUse /help to see list of commands to interact with it XD"
    )

    await state.clear()


    

@router.message(Command("delete"))
async def delete_mevengi(message: Message):
    data = load_data()
    data.pop(str(message.chat.id), None)
    save_data(data)
    print('Successfully deleted! You\'ve just killed innocent animal! Good job!')




#!!! STATS !!!

@router.message(Command('stats'))
async def show_stats(message: Message):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()



    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return

    await update_satiety_and_hygiene(message, False)
    mevengi_data = load_data()

    await message.answer(
        f"Your Mevengi:\n"
        f"Name: {mevengi_data[chat_id]['name']}\n"
        f"Level: {mevengi_data[chat_id]['level']}\n"
        f"Balance: ${mevengi_data[chat_id]['money']}\n"
        f"Satiety: {int(mevengi_data[chat_id]['satiety'])}\n"
        f"Happiness: {mevengi_data[chat_id]['happiness']}\nHygiene status: {mevengi_data[chat_id]['hygiene_status']}\nTap-tap level: {mevengi_data[chat_id]['tap_tap_lvl']}"
    )


@router.message(F.text == 'Hi')
async def how_are_you(message: Message):
    await message.answer("Hello UwU")


#!!! HELP COMMAND !!!

@router.message(Command('help'))
async def command_help(message: Message):
        await message.answer(f"Here is the list of commands:\n\n/stats - shows you statistic of your mevengi.\n/feed - used to feed your mevengi.\n/casino - shows you a list of commands for casino.\n/change_name - allows you to change your mevengi's name.\n/tap_tap - get easy money.\n/pet - pet Mevengi and make him happier.")



#!!! NAME CHANGE !!!

@router.message(Command('change_name'))
async def name_change_request(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()

    if chat_id not in mevengi_data:
        await message.answer("Seems like you have no mevengis yet. Use /create to create one!")
        return

    await state.set_state(NameChange.new_name)
    await message.answer("Enter new name")

@router.message(NameChange.new_name)
async def change_name(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()
    await state.update_data(new_name=message.text)
    fsm_data = await state.get_data()
    mevengi_data[chat_id]['name'] = fsm_data['new_name']
    save_data(mevengi_data)
    await message.answer("You successfully changed your mevengi's name!")
    await state.clear()



#!!! FEED !!!

@router.message(Command('feed'))
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

        mevengi_data[chat_id]['level_up'] = str(level_up)

        save_data(mevengi_data)
    else:
        await message.answer("Seems like you are too poor for this...")



#!!! PET !!!

@router.message(Command('pet'))
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

@router.message(Command('bath'))
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

    await update_satiety_and_hygiene(message, True)
    mevengi_data = load_data()

    await message.answer(f"You washed your Mevengi! Now it's hygiene status is: {mevengi_data[chat_id]['hygiene_status']}.")
    

    save_data(mevengi_data)


#!!! CASINO !!!

@router.message(Command('casino'))
async def command_casino(message: Message):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()
    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return   
            
    if mevengi_data[chat_id]['casino_locker']:
         await message.answer('You need level 2 to access this function :)') 
         return     
    
    await update_satiety_and_hygiene(message, False)
    await message.answer(f"Casino commands:\n\n/lottery - shows you lottery rules.\n/number_guess - shows you number guessing rules.\n/paper_scissors_rock - shows you paper-scissors-rock rules.")


#!!! LOTTERY !!!

@router.message(Command('lottery'))
async def command_lottery(message: Message):
        chat_id = str(message.chat.id)
        mevengi_data = load_data()
        if chat_id not in mevengi_data:
            await message.answer("This chat has no Mevengi yet. Use /create to create one!")
            return
        
        await update_satiety_and_hygiene(message, False)

        if mevengi_data[chat_id]['casino_locker']:
         await message.answer('You need level 2 to access this function :)') 
         return  

        await message.answer(f"One lottery ticket costs $20. \n\nWin gives you $200. \nJackpot gives you $10k. \nSuper Jackpot gives you $100k.\n\nChances: \nWin - 8%\nJackpot - 0.2%\nSuper Jackpot - 0.016%\n\nTo buy ticket use /ticket.")

@router.message(Command('ticket'))
async def play_lottery(message: Message):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()

    if chat_id not in mevengi_data:
         await message.answer("Seems like you have no mevengis yet. Use /create to create one!")
         return

    await update_satiety_and_hygiene(message, False)

    if mevengi_data[chat_id]['casino_locker']:
         await message.answer('You need level 2 to access this function :)') 
         return  

    mevengi_data = load_data()
    if int(mevengi_data[chat_id]['money']) >= 20:
        new_money = int(mevengi_data[chat_id]['money']) - 20
        mevengi_data[chat_id]['money'] = str(new_money)
        
        result_ticket = lottery_ticket()
        
        if result_ticket == "super_jackpot":
             new_money = int(mevengi_data[chat_id]['money']) + 100000
             mevengi_data[chat_id]['money'] = str(new_money)
             await message.answer(f"IT'S SUPER JACKPOT!!!!!!!!!\nBalance left: ${mevengi_data[chat_id]['money']}")
        elif result_ticket == "jackpot":
             new_money = int(mevengi_data[chat_id]['money']) + 10000
             mevengi_data[chat_id]['money'] = str(new_money)
             await message.answer(f"IT'S JACKPOT!!!!!!!!!\nBalance left: ${mevengi_data[chat_id]['money']}")
        elif result_ticket == 'win':
             new_money = int(mevengi_data[chat_id]['money']) + 200
             mevengi_data[chat_id]['money'] = str(new_money)
             await message.answer(f"You won!\nBalance left: ${mevengi_data[chat_id]['money']}")
        else:
             await message.answer(f"You lost.\nBalance left: ${mevengi_data[chat_id]['money']}")
        
        save_data(mevengi_data)
        
    else:
        await message.answer("Seems like you are too poor for this...")


#!!! NUMBER GUESS !!!

@router.message(Command('number_guess'))
async def command_number(message: Message):
        chat_id = str(message.chat.id)
        mevengi_data = load_data()
        if chat_id not in mevengi_data:
            await message.answer("Seems like you have no mevengis yet. Use /create to create one!")
            return
        await update_satiety_and_hygiene(message, False)
        if mevengi_data[chat_id]['casino_locker']:
         await message.answer('You need level 2 to access this function :)') 
         return  
        await message.answer(f"Machine randomly generates number from 1 to 10. \nYou can choose either you think the number is greater than 5, lower than 5 or equals 5. \nIf you chose greater than 5 and won you will multiply your bet by 1.7, if you chose lower than 5 and guessed you will double your bet and if you chose 5 and guessed you will get your bet multiplied by 10. \nTo play use /play_guess")



@router.message(Command('play_guess'))
async def play_number(message: Message, state: FSMContext):
        chat_id = str(message.chat.id)
        mevengi_data = load_data()
        if chat_id not in mevengi_data:
            await message.answer("This chat has no Mevengi yet. Use /create to create one!")
            return
        await update_satiety_and_hygiene(message, False)
        if mevengi_data[chat_id]['casino_locker']:
         await message.answer('You need level 2 to access this function :)') 
         return  
        await message.answer(f"Enter the amount you wanna bet.")
        await state.set_state(NumberGuess.bet)
        

    

@router.message(NumberGuess.bet)
async def guess_game(message: Message, state: FSMContext):
     chat_id = str(message.chat.id)
     mevengi_data = load_data()
     if message.text.lower() == 'exit':
        await state.clear()
        await message.answer("You exited the game! You can use /help if needed.")
        return
     await update_satiety_and_hygiene(message, False)
     mevengi_data = load_data()
     if message.text.isdigit():
                bet_money = int(message.text)
                if bet_money <= int(mevengi_data[chat_id]['money']):
                    await message.answer(f"Choose option:\n1. Greater than 5\n2. Lower than 5\n3. Equals 5\nTo choose just send the message with digit of option you chose.")
                    await state.update_data(bet = message.text)
                    new_balance = int(mevengi_data[chat_id]['money']) - bet_money
                    mevengi_data[chat_id]['money'] = str(new_balance)
                    save_data(mevengi_data)
                    await state.set_state(NumberGuess.guess)
                    
                else:
                    await message.answer("You are too poor for this big bet. Type-in 'exit' if u wanna exit game or place some lower bet..")
     else:
                await message.answer("Enter valid number.")



@router.message(NumberGuess.guess)
async def guess_game_stage2(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    await update_satiety_and_hygiene(message, False)
    mevengi_data = load_data()
    fsm_data = await state.get_data()
    if message.text.isdigit() and 1 <= int(message.text) <= 3:
         result = random_number_generator()
         if message.text == result:
              if result == '1':
                   new_balance = int(int(mevengi_data[chat_id]['money']) + (int(fsm_data['bet']) * 1.8))
                   mevengi_data[chat_id]['money'] = str(new_balance)
                   await message.answer(f"You guessed!!! Your new balance is ${mevengi_data[chat_id]['money']}!\nIf you wanna play again use /play_guess")
                   save_data(mevengi_data)
                   await state.clear()
                   
              elif result == '2':
                   new_balance = int(mevengi_data[chat_id]['money']) + (int(fsm_data['bet']) * 2)
                   mevengi_data[chat_id]['money'] = str(new_balance)
                   await message.answer(f"You guessed!!! Your new balance is ${mevengi_data[chat_id]['money']}!\nIf you wanna play again use /play_guess")
                   save_data(mevengi_data)
                   await state.clear()
              elif result == '3':
                   new_balance = int(mevengi_data[chat_id]['money']) + (int(fsm_data['bet']) * 10)
                   mevengi_data[chat_id]['money'] = str(new_balance)
                   await message.answer(f"You guessed!!! Your new balance is ${mevengi_data[chat_id]['money']}!\nIf you wanna play again use /play_guess")
                   save_data(mevengi_data)
                   await state.clear()
         else:
             await message.answer(f"I'm so sorry, but you lost. Balance left: {mevengi_data[chat_id]['money']}. If u wanna try again use /play_guess")
             await state.clear()
    else:
         await message.answer("Enter valid option(1, 2 or 3)!")


     


#!!! PAPER SCISSORS ROCK !!!


@router.message(Command('paper_scissors_rock'))
async def paper_scissors_rock_rules(message: Message):
        chat_id = str(message.chat.id)
        mevengi_data = load_data()
        if chat_id not in mevengi_data:
            await message.answer("This chat has no Mevengi yet. Use /create to create one!")
            return
        await update_satiety_and_hygiene(message, False)
        if mevengi_data[chat_id]['casino_locker']:
         await message.answer('You need level 2 to access this function :)') 
         return  
        await message.answer(f"This is classic paper-scissors-rock game.\nJust enter amount of your bet.\nIf you won bet will be doubled.\nIf you lost you will lose whole amount.\nIf it's a tie your money will be returned.\nTo play use /play_psr.")

@router.message(Command('play_psr'))
async def play_psr(message: Message, state: FSMContext):
        chat_id = str(message.chat.id)
        mevengi_data = load_data()
        if chat_id not in mevengi_data:
            await message.answer("This chat has no Mevengi yet. Use /create to create one!")
            return
        await update_satiety_and_hygiene(message, False)
        if mevengi_data[chat_id]['casino_locker']:
         await message.answer('You need level 2 to access this function :)') 
         return  
        await message.answer(f"Enter the amount of your bet.")
        await state.set_state(PaperScissorsRock.bet)


@router.message(PaperScissorsRock.bet)
async def bet_psr(message: Message, state: FSMContext):
     chat_id = str(message.chat.id)
     await update_satiety_and_hygiene(message, False)
     mevengi_data = load_data()
     if message.text.lower() == 'exit':
        await state.clear()
        await message.answer("You exited the game! You can use /help if needed.")
        return

     if message.text.isdigit():
                bet_money = int(message.text)
                if bet_money <= int(mevengi_data[chat_id]['money']):
                    await message.answer(f"Type your choice(just a number):\n1.Paper.\n2.Scissors.\n3.Rock.")
                    await state.update_data(bet = message.text)
                    new_balance = int(mevengi_data[chat_id]['money']) - bet_money
                    mevengi_data[chat_id]['money'] = str(new_balance)
                    save_data(mevengi_data)
                    await state.set_state(PaperScissorsRock.choice)
                    
                else:
                    await message.answer("You are too poor for this big bet. Type-in 'exit' if u wanna exit game or place some lower bet.")
     else:
                await message.answer("Enter valid number.")


@router.message(PaperScissorsRock.choice)
async def guess_game_stage2(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    await update_satiety_and_hygiene(message, False)
    mevengi_data = load_data()
    fsm_data = await state.get_data()

    if message.text.isdigit() and 1 <= int(message.text) <= 3:
         result = choice_psr()
         if message.text == "1":
              if result == 'paper':
                   new_balance = int(int(mevengi_data[chat_id]['money']) + int(fsm_data['bet']))
                   mevengi_data[chat_id]['money'] = str(new_balance)
                   await message.answer(f"You tie! Your balance is ${mevengi_data[chat_id]['money']}!\nIf you wanna play again use /play_psr")
                   save_data(mevengi_data)
                   await state.clear()
                   
              elif result == 'scissors':
                   await message.answer(f"You lost. Your balance is ${mevengi_data[chat_id]['money']}!\nIf you wanna play again use /play_psr")
                   await state.clear()
              
              elif result == 'rock':
                   
                   new_balance = int(int(mevengi_data[chat_id]['money']) + (int(fsm_data['bet']) * 2))
                   mevengi_data[chat_id]['money'] = str(new_balance)
                   await message.answer(f"You won!!! Your balance is ${mevengi_data[chat_id]['money']}!\nIf you wanna play again use /play_psr")
                   save_data(mevengi_data)
                   await state.clear()
         elif message.text == "2":
              if result == 'paper':
                   new_balance = int(int(mevengi_data[chat_id]['money']) + (int(fsm_data['bet']) * 2))
                   mevengi_data[chat_id]['money'] = str(new_balance)
                   await message.answer(f"You won!!! Your balance is ${mevengi_data[chat_id]['money']}!\nIf you wanna play again use /play_psr")
                   save_data(mevengi_data)
                   await state.clear()
                   
              elif result == 'scissors':
                   new_balance = int(int(mevengi_data[chat_id]['money']) + int(fsm_data['bet']))
                   mevengi_data[chat_id]['money'] = str(new_balance)
                   await message.answer(f"You tie! Your balance is ${mevengi_data[chat_id]['money']}!\nIf you wanna play again use /play_psr")
                   save_data(mevengi_data)
                   await state.clear()
              
              elif result == 'rock':
                   await message.answer(f"You lost. Your balance is ${mevengi_data[chat_id]['money']}!\nIf you wanna play again use /play_psr")
                   await state.clear()
         
         elif message.text == "3":
              if result == 'paper':
                   await message.answer(f"You lost. Your balance is ${mevengi_data[chat_id]['money']}!\nIf you wanna play again use /play_psr")
                   await state.clear()

              elif result == 'scissors':
                   new_balance = int(int(mevengi_data[chat_id]['money']) + (int(fsm_data['bet']) * 2))
                   mevengi_data[chat_id]['money'] = str(new_balance)
                   await message.answer(f"You won!!! Your balance is ${mevengi_data[chat_id]['money']}!\nIf you wanna play again use /play_psr")
                   save_data(mevengi_data)
                   await state.clear()
              
              elif result == 'rock':
                  new_balance = int(int(mevengi_data[chat_id]['money']) + int(fsm_data['bet']))
                  mevengi_data[chat_id]['money'] = str(new_balance)
                  await message.answer(f"You tie! Your balance is ${mevengi_data[chat_id]['money']}!\nIf you wanna play again use /play_psr")
                  save_data(mevengi_data)
                  await state.clear() 


                   
    else:
         await message.answer("Enter valid option(1, 2 or 3)!")




#!!! TAP-TAP !!!


@router.message(Command('tap_tap'))
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


@router.message(Command('upgrade_tap'))
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

@router.message(TapUpgrade.choice)
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

    