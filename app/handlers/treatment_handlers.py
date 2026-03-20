from aiogram import F, Router, html, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.functions import save_data, load_data, time_updates, inventory_show
from app.classes import Feeding
from keyboards import bath_again_keyboard, feed_again_keyboard, taking_care, pet_again_keyboard, menu_redirect, nofood_kb
from aiogram import Bot



#REST OF STUFF

router_treatment = Router()

#!!! FEED !!!

@router_treatment.callback_query(F.data == 'feed')
async def feed(callback: types.CallbackQuery, state: FSMContext):

    chat_id = str(callback.message.chat.id)
    await time_updates(callback.message, False, False)
    mevengi_data = load_data() 

    if mevengi_data[chat_id]['satiety'] >= 100:
         await callback.message.edit_text("Your mevengi is not hungry!", reply_markup=menu_redirect)
         return

    if not mevengi_data[chat_id]['inventory']:
        await callback.message.edit_text(f"Your inventory is empty right now!", reply_markup=nofood_kb)
        return
    
    inventory = inventory_show(callback.message)
    
    await callback.message.edit_text(f"🎒Your inventory: \n\n{inventory}\nEnter the name of food you wanna use to feed Mevengi with.")

    await state.set_state(Feeding.food)

    save_data(mevengi_data) 


@router_treatment.message(Feeding.food)
async def choice_food(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    await time_updates(message, False, False)
    mevengi_data = load_data()
    if message.text.lower() == 'exit':
        await state.clear()
        await message.answer("You exited the feeding state!", reply_markup=menu_redirect)
        return
    
    if message.text.lower() in mevengi_data[chat_id]['inventory']:
        choice = message.text.lower()
        match choice:
            case "burgers":
                mevengi_data[chat_id]['inventory']['burgers'] -= 1
                if mevengi_data[chat_id]['inventory']['burgers'] == 0:
                    mevengi_data[chat_id]['inventory'].pop("burgers")

                mevengi_data[chat_id]['satiety'] += 10


            case "salads":
                mevengi_data[chat_id]['inventory']['salads'] -= 1
                if mevengi_data[chat_id]['inventory']['salads'] == 0:
                    mevengi_data[chat_id]['inventory'].pop("salads")

                mevengi_data[chat_id]['satiety'] += 10

            case "coka-locas":
                mevengi_data[chat_id]['inventory']['coka-locas'] -= 1
                if mevengi_data[chat_id]['inventory']['coka-locas'] == 0:
                    mevengi_data[chat_id]['inventory'].pop("coka-locas")

                mevengi_data[chat_id]['satiety'] += 3

            case "pizzas":
                mevengi_data[chat_id]['inventory']['pizzas'] -= 1
                if mevengi_data[chat_id]['inventory']['pizzas'] == 0:
                    mevengi_data[chat_id]['inventory'].pop("pizzas")

                mevengi_data[chat_id]['satiety'] += 25

        level_up = int(mevengi_data[chat_id]['level_up']) + 10
        
        if level_up >= 100:
            new_level = int(mevengi_data[chat_id]['level']) + 1
            mevengi_data[chat_id]['level'] = new_level
            level_up -= 100
            await message.answer(f"🆙Your mevengi has grew up!🆙\nNow it's lvl.{new_level}")
            if new_level == 2:
                mevengi_data[chat_id]['casino_locker'] = False
                await message.answer("You have unlocked casino now! Have fun!")
            if new_level == 5:
                mevengi_data[chat_id]['bank_locker'] = False
                await message.answer("You have unlocked bank now!") 

        mevengi_data[chat_id]['level_up'] = str(level_up)
        
        await message.answer(f"You fed the Mevengi! 💖\n"
                             f"Satiety: {int(mevengi_data[chat_id]['satiety'])}",
                             reply_markup=feed_again_keyboard
        )
        await state.clear()
        save_data(mevengi_data)
    else:
        await message.answer("Enter valid option or 'exit' to exit this menu!")



#!!! PET !!!

@router_treatment.callback_query(F.data == 'pet')
async def bath_again(callback: types.CallbackQuery):
    chat_id = str(callback.message.chat.id)
    await time_updates(callback.message, False, True)
    mevengi_data = load_data() 

    if mevengi_data[chat_id]['happiness'] < 100:
        mevengi_data[chat_id]['happiness'] += 5
        
    if mevengi_data[chat_id]['happiness'] > 100:
            mevengi_data[chat_id]['happiness'] = 100


    try:
        await callback.message.edit_text(f"You pet your Mevengi 🤩\nHappiness: {mevengi_data[chat_id]['happiness']}", parse_mode=None, reply_markup=pet_again_keyboard)
    except:
        pass

    save_data(mevengi_data)




#!!! BATH !!!

@router_treatment.callback_query(F.data == 'bath')
async def bath_callback(callback: types.CallbackQuery):
    chat_id = str(callback.message.chat.id)
    await time_updates(callback.message, True, True)
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
    try:
        await callback.message.edit_text(f"You washed your Mevengi 🧼!\nNow it's hygiene status is: {mevengi_data[chat_id]['hygiene_status']}.", reply_markup=bath_again_keyboard)
    except:
        pass

    save_data(mevengi_data)






@router_treatment.callback_query(F.data == 'care')
async def feed(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Choose option to take care of your mevengi🥰", reply_markup=taking_care)