from aiogram import F, Router, html
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.functions import save_data, load_data, time_updates, inventory_show
from app.classes import Shopping

router_shopinventory = Router()





@router_shopinventory.message(Command('inventory'))
async def inventory(message: Message):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()  
    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await time_updates(message, False)

    mevengi_data = load_data() 

    if not mevengi_data[chat_id]['inventory']:
        await message.answer(f"Your inventory is empty right now!\nYou can use /shop to buy some food.")
        return
    
    inventory = inventory_show(message)
    
    await message.answer(f"Your inventory: \n{inventory}")
    save_data(mevengi_data)




@router_shopinventory.message(Command('shop'))
async def shop(message: Message):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()  
    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await time_updates(message, False)

    mevengi_data = load_data() 

    await message.answer(f"Your balance: ${mevengi_data[chat_id]['money']}.\n/food - see the food list.")
    
    save_data(mevengi_data)


@router_shopinventory.message(Command('food'))
async def food_buy(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    mevengi_data = load_data()  
    if chat_id not in mevengi_data:
        await message.answer("This chat has no Mevengi yet. Use /create to create one!")
        return
    
    await time_updates(message, False)

    mevengi_data = load_data() 

    await message.answer(f"Available products to buy:\n1. Burger(🍗: 10 💲: 7)\n2. Pizza(🍗: 25 💲: 15)\n3. Salad(🍗: 10 💲: 9)\n4. Coca-loca(🍗: 3 💲: 3)\nEnter the number of product you wanna buy, or 'exit' to exit menu.")
    
    await state.set_state(Shopping.product)

    save_data(mevengi_data)

@router_shopinventory.message(Shopping.product)
async def food_buy(message: Message, state: FSMContext):
    await time_updates(message, False)
    mevengi_data = load_data() 

    if message.text.lower() == 'exit':
        await state.clear()
        await message.answer("You exited the menu! You can use /help if needed.")
        return
     
     
    if message.text.isdigit() and 1<=int(message.text)<=4:
                await state.update_data(product = message.text) 
                await message.answer("How many of this product do you want?")
                await state.set_state(Shopping.quantity)
                
    else:
                await message.answer("Enter valid option.")
    

    save_data(mevengi_data)



@router_shopinventory.message(Shopping.quantity)
async def food_buy(message: Message, state: FSMContext):
    chat_id = str(message.chat.id)
    await time_updates(message, False)
    mevengi_data = load_data() 

    if message.text.lower() == 'exit':
        await state.clear()
        await message.answer("You exited the menu! You can use /help if needed.")
        return
    
    if message.text.lower() == '/back':
        await state.clear()
        await message.answer("Available products to buy:\n1. Burger(🍗: 10 💲: 7)\n2. Pizza(🍗: 25 💲: 15)\n3. Salad(🍗: 10 💲: 9)\n4. Coca-loca(🍗: 3 💲: 3)\nEnter the number of product you wanna buy, or 'exit' to exit menu.")
        await state.set_state(Shopping.product)
        return
     
     
    if message.text.isdigit():
                fsm_data = await state.get_data()
                quantity = int(message.text)
                if fsm_data['product'] == "1":
                        price = 7
                elif fsm_data['product'] == "2":
                        price = 15
                elif fsm_data['product'] == "3":
                        price = 9
                elif fsm_data['product'] == "4":
                        price = 3
                
                total_price = quantity * price

                if int(mevengi_data[chat_id]['money']) < total_price:
                        await message.answer(f"You don't have enough money! Your balance is ${mevengi_data[chat_id]['money']}, while total price is ${total_price}. Try lower quantity or /back to choose different product or enter 'exit' to exit menu.")
                        return
                
                new_balance = int(mevengi_data[chat_id]['money']) - total_price

                mevengi_data[chat_id]['money'] = str(new_balance)

                if fsm_data['product'] == "1":
                        name_product = "burger"
                        if "burgers" not in mevengi_data[chat_id]['inventory']:
                            mevengi_data[chat_id]['inventory']['burgers'] = quantity  
                        else:
                            mevengi_data[chat_id]['inventory']['burgers'] += quantity 
                elif fsm_data['product'] == "2":
                        name_product = "pizza"
                        if "pizzas" not in mevengi_data[chat_id]['inventory']:
                            mevengi_data[chat_id]['inventory']['pizzas'] = quantity  
                        else:
                            mevengi_data[chat_id]['inventory']['pizzas'] += quantity 
                elif fsm_data['product'] == "3":
                        name_product = "salad"
                        if "salads" not in mevengi_data[chat_id]['inventory']:
                            mevengi_data[chat_id]['inventory']['salads'] = quantity  
                        else:
                            mevengi_data[chat_id]['inventory']['salads'] += quantity 
                elif fsm_data['product'] == "4":
                        name_product = "coka-loca"
                        if "coka-locas" not in mevengi_data[chat_id]['inventory']:
                            mevengi_data[chat_id]['inventory']['coka-locas'] = quantity  
                        else:
                            mevengi_data[chat_id]['inventory']['coka-locas'] += quantity 
                
                await message.answer(f"You successfully purchased {quantity} of {name_product}!")

                
    else:
                await message.answer("Enter valid option.")
    

    save_data(mevengi_data)
