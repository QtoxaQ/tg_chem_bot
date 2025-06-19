from aiogram.fsm.state import StatesGroup, State


class MyStates(StatesGroup):
    wait_chembl_id = State()
    wait_name = State()
    wait_inchi = State()

    find_similar = State()
    set_count = State()
    choose_type = State()

    smiles = False
    data = None
    count = 5
