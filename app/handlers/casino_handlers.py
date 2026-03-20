from aiogram import F, Router, html, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.functions import save_data, load_data, time_updates, choice_psr, random_number_generator, lottery_ticket
from app.classes import NumberGuess, PaperScissorsRock
from keyboards import menu_redirect, casino_kb, lottery_kb, again_lottery_kb, guess_kb, casino_back_kb  , again_guess_kb, psr_kb, again_psr_kb

router_casino = Router()



#!!! CASINO !!!

@router_casino.callback_query(F.data == 'casino')
async def command_casino(callback: types.CallbackQuery):
    chat_id = str(callback.message.chat.id) 
    await time_updates(callback.message, False, True)
    mevengi_data = load_data()
            
    if mevengi_data[chat_id]['casino_locker']:
         await callback.message.edit_text('You need level 2 to access this function :)', reply_markup=menu_redirect) 
         return     
    
    await callback.message.edit_text(f"🎰 Casino 🎰", reply_markup=casino_kb)


#!!! LOTTERY !!!

@router_casino.callback_query(F.data == 'lottery')
async def command_lottery(callback: types.CallbackQuery):
        
        await time_updates(callback.message, False, True)

        await callback.message.edit_text(f"One lottery ticket costs $20\n\n🤑 Win gives you $200. \n💸 Jackpot gives you $10k. \n💸💸💸 Super Jackpot gives you $100k.\n\nChances: \nWin - 8%\nJackpot - 0.2%\nSuper Jackpot - 0.016%\n\nTry your luck!", reply_markup=lottery_kb)

@router_casino.callback_query(F.data == 'ticket')
async def play_lottery(callback: types.CallbackQuery):
    chat_id = str(callback.message.chat.id)
    await time_updates(callback.message, False, True)
    mevengi_data = load_data() 

    if int(mevengi_data[chat_id]['money']) >= 20:
        new_money = int(mevengi_data[chat_id]['money']) - 20
        mevengi_data[chat_id]['money'] = str(new_money)
        
        result_ticket = lottery_ticket()
        
        if result_ticket == "super_jackpot":
             new_money = int(mevengi_data[chat_id]['money']) + 100000
             mevengi_data[chat_id]['money'] = str(new_money)
             try:
                  await callback.message.edit_text(f"💸💸💸IT'S SUPER JACKPOT💸💸💸\nBalance left: ${mevengi_data[chat_id]['money']}", reply_markup=again_lottery_kb)
             except:
                  pass
        elif result_ticket == "jackpot":
             new_money = int(mevengi_data[chat_id]['money']) + 10000
             mevengi_data[chat_id]['money'] = str(new_money)
             try:
               await callback.message.edit_text(f"💸IT'S JACKPOT💸\nBalance left: ${mevengi_data[chat_id]['money']}", reply_markup=again_lottery_kb)
             except:
               pass
        elif result_ticket == 'win':
             new_money = int(mevengi_data[chat_id]['money']) + 200
             mevengi_data[chat_id]['money'] = str(new_money)
             try:
                  await callback.message.edit_text(f"You won 🤑\nBalance left: ${mevengi_data[chat_id]['money']}", reply_markup=again_lottery_kb)
             except:
                  pass
        else:
             await callback.message.edit_text(f"You lost 😔\nBalance left: ${mevengi_data[chat_id]['money']}", reply_markup=again_lottery_kb)
        
        save_data(mevengi_data)
        
    else:
        await callback.message.edit_text("Seems like you are too poor for this...", reply_markup=menu_redirect)


#!!! NUMBER GUESS !!!

@router_casino.callback_query(F.data == 'guess')
async def command_number(callback: types.CallbackQuery):
        
        await time_updates(callback.message, False, True)
 
        await callback.message.edit_text(f"Machine randomly generates number from 1 to 10 ❔ \n\nYou can choose either you think the number is greater than 5, lower than 5 or equals 5. \nIf you chose greater than 5 and won you will multiply your bet by 1.7, if you chose lower than 5 and guessed you will double your bet and if you chose 5 and guessed you will get your bet multiplied by 10.", reply_markup=guess_kb)



@router_casino.callback_query(F.data == 'guess_play')
async def play_number(callback: types.CallbackQuery, state: FSMContext):
        
        await time_updates(callback.message, False, True)

        await callback.message.edit_text(f"Enter the amount you wanna bet.")
        await state.set_state(NumberGuess.bet)
        

    

@router_casino.message(NumberGuess.bet)
async def guess_game(message: Message, state: FSMContext):
     chat_id = str(message.chat.id)
     mevengi_data = load_data()
     if message.text.lower() == 'exit':
        await state.clear()
        await message.answer("You exited the game!", reply_markup=casino_back_kb)
        return
     await time_updates(message, False, True)
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



@router_casino.message(NumberGuess.guess)
async def guess_game_stage2(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    await time_updates(message, False, True)
    mevengi_data = load_data()
    fsm_data = await state.get_data()
    if message.text.isdigit() and 1 <= int(message.text) <= 3:
         result = random_number_generator()
         if message.text == result:
              if result == '1':
                   new_balance = int(int(mevengi_data[chat_id]['money']) + (int(fsm_data['bet']) * 1.8))
                   mevengi_data[chat_id]['money'] = str(new_balance)
                   await message.answer(f"You guessed!!! Your new balance is ${mevengi_data[chat_id]['money']}!", reply_markup=again_guess_kb)
                   save_data(mevengi_data)
                   await state.clear()
                   
              elif result == '2':
                   new_balance = int(mevengi_data[chat_id]['money']) + (int(fsm_data['bet']) * 2)
                   mevengi_data[chat_id]['money'] = str(new_balance)
                   await message.answer(f"You guessed!!! Your new balance is ${mevengi_data[chat_id]['money']}!", reply_markup=again_guess_kb)
                   save_data(mevengi_data)
                   await state.clear()
              elif result == '3':
                   new_balance = int(mevengi_data[chat_id]['money']) + (int(fsm_data['bet']) * 10)
                   mevengi_data[chat_id]['money'] = str(new_balance)
                   await message.answer(f"You guessed!!! Your new balance is ${mevengi_data[chat_id]['money']}!", reply_markup=again_guess_kb)
                   save_data(mevengi_data)
                   await state.clear()
         else:
             await message.answer(f"I'm so sorry, but you lost. Balance left: {mevengi_data[chat_id]['money']}.", reply_markup=again_guess_kb)
             await state.clear()
    else:
         await message.answer("Enter valid option(1, 2 or 3)!")


     


#!!! PAPER SCISSORS ROCK !!!


@router_casino.callback_query(F.data == 'psr')
async def paper_scissors_rock_rules(callback: types.CallbackQuery):
        
        await time_updates(callback.message, False, True)

        await callback.message.edit_text(f"This is classic paper-scissors-rock game ✂️📄🪨\n\nJust enter amount of your bet.\nIf you won bet will be doubled.\nIf you lost you will lose whole amount.\nIf it's a tie your money will be returned.", reply_markup=psr_kb)

@router_casino.callback_query(F.data == 'psr_play')
async def play_psr(callback: types.CallbackQuery, state: FSMContext):
        
        await time_updates(callback.message, False, True)

        await callback.message.edit_text(f"Enter the amount of your bet.")
        await state.set_state(PaperScissorsRock.bet)


@router_casino.message(PaperScissorsRock.bet)
async def bet_psr(message: Message, state: FSMContext):
     chat_id = str(message.chat.id)
     await time_updates(message, False, True)
     mevengi_data = load_data()
     if message.text.lower() == 'exit':
        await state.clear()
        await message.answer("You exited the game!", reply_markup=casino_back_kb)
        return

     if message.text.isdigit():
                bet_money = int(message.text)
                if bet_money <= int(mevengi_data[chat_id]['money']):
                    await message.answer(f"Type your choice(just a number):\n1. Paper📄\n2. Scissors✂️\n3. Rock🪨")
                    await state.update_data(bet = message.text)
                    new_balance = int(mevengi_data[chat_id]['money']) - bet_money
                    mevengi_data[chat_id]['money'] = str(new_balance)
                    save_data(mevengi_data)
                    await state.set_state(PaperScissorsRock.choice)
                    
                else:
                    await message.answer("You are too poor for this big bet. Type-in 'exit' if u wanna exit game or place some lower bet.")
     else:
                await message.answer("Enter valid number.")


@router_casino.message(PaperScissorsRock.choice)
async def guess_game_stage2(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    await time_updates(message, False, True)
    mevengi_data = load_data()
    fsm_data = await state.get_data()

    if message.text.isdigit() and 1 <= int(message.text) <= 3:
         result = choice_psr()
         if message.text == "1":
              if result == 'paper':
                   new_balance = int(int(mevengi_data[chat_id]['money']) + int(fsm_data['bet']))
                   mevengi_data[chat_id]['money'] = str(new_balance)
                   await message.answer(f"You tie! Your balance is ${mevengi_data[chat_id]['money']}!", reply_markup=again_psr_kb)
                   save_data(mevengi_data)
                   await state.clear()
                   
              elif result == 'scissors':
                   await message.answer(f"You lost. Your balance is ${mevengi_data[chat_id]['money']}!", reply_markup=again_psr_kb)
                   await state.clear()
              
              elif result == 'rock':
                   
                   new_balance = int(int(mevengi_data[chat_id]['money']) + (int(fsm_data['bet']) * 2))
                   mevengi_data[chat_id]['money'] = str(new_balance)
                   await message.answer(f"You won!!! Your balance is ${mevengi_data[chat_id]['money']}!", reply_markup=again_psr_kb)
                   save_data(mevengi_data)
                   await state.clear()
         elif message.text == "2":
              if result == 'paper':
                   new_balance = int(int(mevengi_data[chat_id]['money']) + (int(fsm_data['bet']) * 2))
                   mevengi_data[chat_id]['money'] = str(new_balance)
                   await message.answer(f"You won!!! Your balance is ${mevengi_data[chat_id]['money']}!", reply_markup=again_psr_kb)
                   save_data(mevengi_data)
                   await state.clear()
                   
              elif result == 'scissors':
                   new_balance = int(int(mevengi_data[chat_id]['money']) + int(fsm_data['bet']))
                   mevengi_data[chat_id]['money'] = str(new_balance)
                   await message.answer(f"You tie! Your balance is ${mevengi_data[chat_id]['money']}!", reply_markup=again_psr_kb)
                   save_data(mevengi_data)
                   await state.clear()
              
              elif result == 'rock':
                   await message.answer(f"You lost. Your balance is ${mevengi_data[chat_id]['money']}!", reply_markup=again_psr_kb)
                   await state.clear()
         
         elif message.text == "3":
              if result == 'paper':
                   await message.answer(f"You lost. Your balance is ${mevengi_data[chat_id]['money']}!", reply_markup=again_psr_kb)
                   await state.clear()

              elif result == 'scissors':
                   new_balance = int(int(mevengi_data[chat_id]['money']) + (int(fsm_data['bet']) * 2))
                   mevengi_data[chat_id]['money'] = str(new_balance)
                   await message.answer(f"You won!!! Your balance is ${mevengi_data[chat_id]['money']}!", reply_markup=again_psr_kb)
                   save_data(mevengi_data)
                   await state.clear()
              
              elif result == 'rock':
                  new_balance = int(int(mevengi_data[chat_id]['money']) + int(fsm_data['bet']))
                  mevengi_data[chat_id]['money'] = str(new_balance)
                  await message.answer(f"You tie! Your balance is ${mevengi_data[chat_id]['money']}!", reply_markup=again_psr_kb)
                  save_data(mevengi_data)
                  await state.clear() 


                   
    else:
         await message.answer("Enter valid option(1, 2 or 3)!")