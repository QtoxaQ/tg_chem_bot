from aiogram import Router, types
from aiogram.filters import Command


router = Router()


@router.message(Command('start'))
async def start(message: types.Message):
    await message.answer('''
Привет! Я химический бот.
Вот, что я умею:
1) Находить smiles молекул;
2) Искать похожие молекулы;
3) Рассчитывать физико-химические дескрипторы молекул.

Больше информации по команде /help
''')


@router.message(Command('help'))
async def help(message: types.Message):
    await message.answer('Вы можете использовать следующие команды:')
    await message.answer('''/start
Выводит приветственное сообщение с кратким описанием.''')

    await message.answer('''/get_smiles
Производит поиск smiles молекулы по одному из параметров на выбор:
   - по названию;
   - по ID;
   - по INCHI.''')

    await message.answer('''/find_similar
Ищет молекулы, похожие на заданную (сходство не менее 70%).
Поиск возможен по названию и по smiles.''')

    await message.answer('''/molecular_descriptors
Расчитывает молекулярные дескрипторы для последней найденной молекулы.''')
