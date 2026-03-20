from aiogram import F, Router, html, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.functions import save_data, load_data, time_updates
from app.classes import Banking
from keyboards import menu_redirect, bank_kb, back_bank_kb


router_bank = Router()


@router_bank.callback_query(F.data == 'bank')
async def bank_menu(callback: types.CallbackQuery):
    chat_id = str(callback.message.chat.id) 
    await time_updates(callback.message, False, True)
    mevengi_data = load_data() 

    if mevengi_data[chat_id]['bank_locker']:
         await callback.message.edit_text(f"This section unlocks on level 5!", reply_markup=menu_redirect)
         save_data(mevengi_data)
         return

    await callback.message.edit_text(f"Here is your bank account 🏦\n\nBalance 💳: ${int(mevengi_data[chat_id]['bank_money'])}", reply_markup=bank_kb)
    
    
    save_data(mevengi_data)


@router_bank.callback_query(F.data == 'deposit')
async def deposit(callback: types.CallbackQuery, state: FSMContext):

    await time_updates(callback.message, False, True)

    await callback.message.edit_text(f"How much money you want to deposit? Enter the number.")

    await state.set_state(Banking.deposit)

@router_bank.message(Banking.deposit)
async def deposit_second(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    
    await time_updates(message, False, True)

    mevengi_data = load_data() 

    if message.text.lower() == 'exit':
        await state.clear()
        await message.answer("You exited the deposit state!", reply_markup=back_bank_kb)
        return
    
    if message.text.isdigit():
                deposit = int(message.text)
                if deposit <= int(mevengi_data[chat_id]['money']):
                    new_balance = int(mevengi_data[chat_id]['money']) - deposit
                    mevengi_data[chat_id]['bank_money'] += deposit
                    mevengi_data[chat_id]['money'] = str(new_balance)
                    save_data(mevengi_data)
                    await state.clear()
                    await message.answer(f"You deposited ${deposit}! Money on your account: ${int(mevengi_data[chat_id]['bank_money'])}.", reply_markup=back_bank_kb)
                    mevengi_data[chat_id]['deposited'] = True

                    
                else:
                    await message.answer(f"You are too poor for this big deposit. Current amount of money you have: ${mevengi_data[chat_id]['money']}.\nType-in 'exit' if u wanna exit depositing state or try lower amount.")
    else:
                await message.answer("Enter valid number.")
    
    
    save_data(mevengi_data)



@router_bank.callback_query(F.data == 'withdraw')
async def withdraw(callback: types.CallbackQuery, state: FSMContext):

    chat_id = str(callback.message.chat.id)
    
    await time_updates(callback.message, False, True)

    mevengi_data = load_data() 

    await callback.message.edit_text(f"Your current balance 💳: ${int(mevengi_data[chat_id]['bank_money'])}. How much money you want to withdraw? Enter the number.")
    await state.set_state(Banking.withdraw)
    
    save_data(mevengi_data)


@router_bank.message(Banking.withdraw)
async def withdraw_second(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    
    await time_updates(message, False, True)

    mevengi_data = load_data() 

    if message.text.lower() == 'exit':
        await state.clear()
        await message.answer("You exited the withdraw state!", reply_markup=back_bank_kb)
        return
    
    if message.text.isdigit():
                withdraw = int(message.text)
                if withdraw <= int(mevengi_data[chat_id]['bank_money']):
                    new_balance = int(mevengi_data[chat_id]['money']) + withdraw
                    mevengi_data[chat_id]['bank_money'] -= withdraw
                    mevengi_data[chat_id]['money'] = str(new_balance)
                    save_data(mevengi_data)
                    await state.clear()
                    await message.answer(f"You withdrawed ${withdraw}! Money on your account: ${int(mevengi_data[chat_id]['bank_money'])}.", reply_markup=back_bank_kb)
                    
                else:
                    await message.answer(f"You don't have this much on your account. Current amount you have: ${int(mevengi_data[chat_id]['bank_money'])}.\nType-in 'exit' if u wanna exit depositing state or try lower amount.")
    else:
                await message.answer("Enter valid number.")
    
    
    save_data(mevengi_data)