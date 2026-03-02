from aiogram import F, Router, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import time
from app.functions import save_data, load_data, time_updates
from app.classes import Mevengi, Creation, NameChange



#REST OF STUFF

router = Router()




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
        "tap_tap_lvl": 1,
        "bank_locker": True,
        "bank_money": 0

    }

    save_data(data)

    await message.answer(
        f"Your new Mevengi:\n"
        f"Name: {mevengi.name}\n"
        f"Level: {mevengi.level}\n"
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

    await time_updates(message, False)
    mevengi_data = load_data()

    await message.answer(
        f"Your Mevengi:\n"
        f"Name: {mevengi_data[chat_id]['name']}\n"
        f"Level: {mevengi_data[chat_id]['level']}\n"
        f"Balance: ${mevengi_data[chat_id]['money']}\n"
        f"Satiety: {int(mevengi_data[chat_id]['satiety'])}\n"
        f"Happiness: {mevengi_data[chat_id]['happiness']}\nHygiene status: {mevengi_data[chat_id]['hygiene_status']}\nTap-tap level: {mevengi_data[chat_id]['tap_tap_lvl']}\nMoney on bank account: ${mevengi_data[chat_id]['bank_money']}"
    )


@router.message(F.text == 'Hi')
async def how_are_you(message: Message):
    await message.answer("Hello UwU")


#!!! HELP COMMAND !!!

@router.message(Command('help'))
async def command_help(message: Message):
        await message.answer(f"Here is the list of commands:\n\n/stats - shows you statistic of your mevengi.\n/feed - used to feed your mevengi.\n/casino - shows you a list of commands for casino.\n/change_name - allows you to change your mevengi's name.\n/tap_tap - get easy money.\n/pet - pet Mevengi and make him happier.\n/bath - give your mevengi a bath.")



#!!! NAME CHANGE !!!

@router.message(Command('change_name'))
async def name_change_request(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()

    if chat_id not in mevengi_data:
        await message.answer("Seems like you have no mevengis yet. Use /create to create one!")
        return
    
    if int(mevengi_data[chat_id]['money']) <= 200:
        await message.answer(f"Change of the name costs $200. Your balance is ${int(mevengi_data[chat_id]['money'])}. It's not enough!")
        return
    
    await message.answer(f"Change of the name costs $200. If you are willing to do that use /confirm_change!")


@router.message(Command('confirm_change'))
async def name_change_request(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()

    if chat_id not in mevengi_data:
        await message.answer("Seems like you have no mevengis yet. Use /create to create one!")
        return
    
    await time_updates(message, True)
    mevengi_data = load_data()

    if int(mevengi_data[chat_id]['money']) <= 200:
        await message.answer(f"Change of the name costs $200. Your balance is ${int(mevengi_data[chat_id]['money'])}. It's not enough!")
        return
    
    new_money = int(mevengi_data[chat_id]['money']) - 200
    mevengi_data[chat_id]['money'] = str(new_money)
    save_data(mevengi_data)
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









