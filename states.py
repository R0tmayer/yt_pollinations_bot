from aiogram.fsm.state import State, StatesGroup

class GenStates(StatesGroup):
    menu = State()
    edit_model = State()
    edit_seed = State()
    edit_width = State()
    edit_height = State()
    edit_ref_image = State()
    edit_enhance = State()
    edit_transparent = State()
    wait_file = State() 