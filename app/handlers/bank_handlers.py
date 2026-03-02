from aiogram import F, Router, html
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.functions import save_data, load_data, time_updates
from app.classes import Banking


router_bank = Router()


@router_bank.message(Command('bank'))
async def bank_menu(message: Message):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()  
    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await time_updates(message, False)

    mevengi_data = load_data() 

    if mevengi_data[chat_id]['bank_locker']:
         await message.answer(f"This section unlocks on level 5!")
         save_data(mevengi_data)
         return

    await message.answer(f"Here is your bank account. \nBalance: ${int(mevengi_data[chat_id]['bank_money'])}.\nUse /deposit to put money on your account and get some % every 5 hours. \nUse /withdraw to withdraw money from your deposit.")
    
    
    save_data(mevengi_data)


@router_bank.message(Command('deposit'))
async def deposit(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()  
    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await time_updates(message, False)

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
    
    await time_updates(message, False)

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
                    await message.answer(f"You deposited ${deposit}! Money on your account: ${int(mevengi_data[chat_id]['bank_money'])}.")
                    mevengi_data[chat_id]['deposited'] = True

                    
                else:
                    await message.answer(f"You are too poor for this big deposit. Current amount of money you have: ${mevengi_data[chat_id]['money']}.\nType-in 'exit' if u wanna exit depositing state or try lower amount.")
    else:
                await message.answer("Enter valid number.")
    
    
    save_data(mevengi_data)



@router_bank.message(Command('withdraw'))
async def withdraw(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()  
    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await time_updates(message, False)

    mevengi_data = load_data() 

    if mevengi_data[chat_id]['bank_locker']:
         await message.answer(f"This section unlocks on level 5!")
         save_data(mevengi_data)
         return

    await message.answer(f"Your current balance is ${int(mevengi_data[chat_id]['bank_money'])}. How much money you want to withdraw? Enter the number.")
    await state.set_state(Banking.withdraw)
    
    save_data(mevengi_data)


@router_bank.message(Banking.withdraw)
async def withdraw_second(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    
    await time_updates(message, False)

    mevengi_data = load_data() 

    if message.text.lower() == 'exit':
        await state.clear()
        await message.answer("You exited the withdraw state! You can use /help if needed.")
        return
    
    if message.text.isdigit():
                withdraw = int(message.text)
                if withdraw <= int(mevengi_data[chat_id]['bank_money']):
                    new_balance = int(mevengi_data[chat_id]['money']) + withdraw
                    mevengi_data[chat_id]['bank_money'] -= withdraw
                    mevengi_data[chat_id]['money'] = str(new_balance)
                    save_data(mevengi_data)
                    await state.clear()
                    await message.answer(f"You withdrawed ${withdraw}! Money on your account: ${int(mevengi_data[chat_id]['bank_money'])}.")
                    
                else:
                    await message.answer(f"You don't have this much on your account. Current amount you have: ${int(mevengi_data[chat_id]['bank_money'])}.\nType-in 'exit' if u wanna exit depositing state or try lower amount.")
    else:
                await message.answer("Enter valid number.")
    
    
    save_data(mevengi_data)