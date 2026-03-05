from aiogram import F, Router, html
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.functions import save_data, load_data, time_updates, inventory_show
from app.classes import Feeding




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

    if not mevengi_data[chat_id]['inventory']:
        await message.answer(f"Your inventory is empty right now!\nYou can use /shop to buy some food.")
        return
    
    inventory = inventory_show(message)
    
    await message.answer(f"Your inventory: \n{inventory}\nEnter the name of food you wanna use to feed Mevengi with.")

    await state.set_state(Feeding.food)

    save_data(mevengi_data)

        

@router_treatment.message(Feeding.food)
async def choice_food(message: Message, state: FSMContext):
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
            await message.answer(f"Your mevengi has grew up! Now it's lvl.{new_level}")
            if new_level == 2:
                mevengi_data[chat_id]['casino_locker'] = False
                await message.answer("You have unlocked casino now! Have fun!")
            if new_level == 5:
                mevengi_data[chat_id]['bank_locker'] = False
                await message.answer("You have unlocked bank now!") 

        mevengi_data[chat_id]['level_up'] = str(level_up)
        
        await message.answer(
            f"You fed the Mevengi! 💖\n"
            f"Satiety: {int(mevengi_data[chat_id]['satiety'])}"
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
        mevengi_data[chat_id]['happiness'] += 2
        
    if mevengi_data[chat_id]['happiness'] > 100:
            mevengi_data[chat_id]['happiness'] = 100


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

    await message.answer(f"You washed your Mevengi! Now it's hygiene status is: {mevengi_data[chat_id]['hygiene_status']}.")
    

    save_data(mevengi_data)

