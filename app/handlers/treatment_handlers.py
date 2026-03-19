from aiogram import F, Router, html, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.functions import save_data, load_data, time_updates, inventory_show
from app.classes import Feeding
from keyboards import bath_again_keyboard, feed_again_keyboard
from aiogram import Bot



#REST OF STUFF

router_treatment = Router()

#!!! FEED !!!

@router_treatment.message(Command('feed'))
async def feed(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()

    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await time_updates(message, False, False)

    mevengi_data = load_data() 

    if mevengi_data[chat_id]['satiety'] >= 100:
         await message.answer("Your mevengi is not hungry!")
         return

    if not mevengi_data[chat_id]['inventory']:
        await message.answer(f"Your inventory is empty right now!\nYou can use /shop to buy some food.")
        return
    
    inventory = inventory_show(message)
    
    await message.answer(f"🎒Your inventory: \n\n{inventory}\nEnter the name of food you wanna use to feed Mevengi with.")

    await state.set_state(Feeding.food)

    save_data(mevengi_data)

@router_treatment.callback_query(F.data == 'feed')
async def feed(callback: types.CallbackQuery, state: FSMContext):
    chat_id = str(callback.message.chat.id)
    mevengi_data = load_data()

    if chat_id not in mevengi_data:
        await callback.message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await time_updates(callback.message, False, False)

    mevengi_data = load_data() 
    if mevengi_data[chat_id]['satiety'] >= 100:
         await callback.message.answer("Your mevengi is not hungry!")
         return

    if not mevengi_data[chat_id]['inventory']:
        await callback.message.answer(f"Your inventory is empty right now!\nYou can use /shop to buy some food.")
        return
    
    inventory = inventory_show(callback.message)
    
    await callback.message.answer(f"🎒Your inventory: \n\n{inventory}\nEnter the name of food you wanna use to feed Mevengi with.")

    await state.set_state(Feeding.food)

    save_data(mevengi_data) 

@router_treatment.callback_query(F.data == 'feed_again')
async def feed(callback: types.CallbackQuery, state: FSMContext):
    chat_id = str(callback.message.chat.id)
    mevengi_data = load_data()

    if chat_id not in mevengi_data:
        await callback.message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await time_updates(callback.message, False, False)

    mevengi_data = load_data() 
    if mevengi_data[chat_id]['satiety'] >= 100:
         await callback.message.answer("Your mevengi is not hungry!")
         return

    if not mevengi_data[chat_id]['inventory']:
        await callback.message.edit_text(f"Your inventory is empty right now!\nYou can use /shop to buy some food.")
        return
    
    inventory = inventory_show(callback.message)
    
    await callback.message.edit_text(f"🎒Your inventory: \n\n{inventory}\nEnter the name of food you wanna use to feed Mevengi with.")

    await state.set_state(Feeding.food)

    save_data(mevengi_data)   

@router_treatment.message(Feeding.food)
async def choice_food(message: Message, state: FSMContext, bot: Bot):
    chat_id = str(message.chat.id)
    await time_updates(message, False, False)
    mevengi_data = load_data()
    if message.text.lower() == 'exit':
        await state.clear()
        await message.answer("You exited the feeding state! You can use /help if needed.")
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

@router_treatment.message(Command('pet'))
async def petting(message: Message):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()  
    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await time_updates(message, False, True)

    mevengi_data = load_data() 

    if mevengi_data[chat_id]['happiness'] < 100:
        mevengi_data[chat_id]['happiness'] += 5
        
    if mevengi_data[chat_id]['happiness'] > 100:
            mevengi_data[chat_id]['happiness'] = 100


    await message.answer(f"You pet your Mevengi 🤩\nHappiness: {mevengi_data[chat_id]['happiness']}", parse_mode=None)
    
    save_data(mevengi_data)




#!!! BATH !!!

@router_treatment.message(Command('bath'))
async def bath(message: Message):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()  
    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await time_updates(message, True, True)

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

    await message.answer(f"You washed your Mevengi 🧼!\nNow it's hygiene status is: {mevengi_data[chat_id]['hygiene_status']}.", reply_markup=bath_again_keyboard)
    

    save_data(mevengi_data)

@router_treatment.callback_query(F.data == 'bath')
async def bath_callback(callback: types.CallbackQuery):
    chat_id = str(callback.message.chat.id)
    mevengi_data = load_data()  
    if chat_id not in mevengi_data:
        await callback.message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
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

    await callback.message.answer(f"You washed your Mevengi 🧼!\nNow it's hygiene status is: {mevengi_data[chat_id]['hygiene_status']}.", reply_markup=bath_again_keyboard)
    

    save_data(mevengi_data)


@router_treatment.callback_query(F.data == 'bath_again')
async def bath_again(callback: types.CallbackQuery):
    chat_id = str(callback.message.chat.id)
    mevengi_data = load_data()  
    if chat_id not in mevengi_data:
        await callback.message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
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
        await callback.message.edit_text(f"You washed your Mevengi again 🧼!\nNow it's hygiene status is: {mevengi_data[chat_id]['hygiene_status']}.", reply_markup=bath_again_keyboard)
    except:
         pass

    save_data(mevengi_data)