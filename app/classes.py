from aiogram.fsm.state import StatesGroup, State

class Creation(StatesGroup):
    name = State()

class NumberGuess(StatesGroup):
    bet = State()
    guess = State()

class Mevengi:
    def __init__(self, name, mevengi_id, last_update):
        self.id = mevengi_id
        self.name = name
        self.last_update = last_update
        self.level = 1
        self.money = 100
        self.level_up = 0
        self.satiety = 50
        self.happiness = 100

        

class NameChange(StatesGroup):
    new_name = State()

class PaperScissorsRock(StatesGroup):
    bet = State()
    choice = State()

class TapUpgrade(StatesGroup):
    choice = State()