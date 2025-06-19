from aiogram import types


class Keyboard:
    @property
    def smiles(self):
        keyboard = [[
            types.KeyboardButton(text='По названию'),
            types.KeyboardButton(text='По CHEMBL ID'),
            types.KeyboardButton(text='По INCHI')
            ]]
        return types.ReplyKeyboardMarkup(keyboard=keyboard,
                                         resize_keyboard=True)

    @property
    def similar(self):
        keyboard = [[
            types.InlineKeyboardButton(text='По названию',
                                       callback_data='name'),
            types.InlineKeyboardButton(text='По smiles',
                                       callback_data='smiles')
            ]]
        return types.InlineKeyboardMarkup(inline_keyboard=keyboard)

    @property
    def select_type(self):
        keyboard = [[
            types.InlineKeyboardButton(text='SDF',
                                       callback_data='sdf'),
            types.InlineKeyboardButton(text='SMI',
                                       callback_data='smi'),
            types.InlineKeyboardButton(text='PNG',
                                       callback_data='png')
            ]]
        return types.InlineKeyboardMarkup(inline_keyboard=keyboard)

    @property
    def choose_type(self):
        keyboard = [[
            types.InlineKeyboardButton(text='В чате',
                                       callback_data='chat'),
            types.InlineKeyboardButton(text='smi',
                                       callback_data='smi'),
            types.InlineKeyboardButton(text='txt',
                                       callback_data='txt')
            ]]
        return types.InlineKeyboardMarkup(inline_keyboard=keyboard)
