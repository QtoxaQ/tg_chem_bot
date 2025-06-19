from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from chembl_webresource_client.new_client import new_client
from aiogram.fsm.context import FSMContext
from states import MyStates
from .keyboard import Keyboard
from io import StringIO, BytesIO


router = Router()


@router.message(Command('find_similar'))
async def similar(message: types.Message):
    await message.answer('Выберите тип поиска',
                         reply_markup=Keyboard().similar)


@router.callback_query(F.data == 'name')
async def smiles_by_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        'Введите название молекулы (на английском)')
    MyStates.smiles = False
    await state.set_state(MyStates.find_similar)  # поменять местами с нижней, когда починю файловый тип
    # await state.set_state(MyStates.set_count)
    await callback.answer()


@router.callback_query(F.data == 'smiles')
async def mol_smiles(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите smiles молекулы')
    MyStates.smiles = True
    await state.set_state(MyStates.find_similar)
    # await state.set_state(MyStates.set_count)
    await callback.answer()


@router.message(StateFilter(MyStates.find_similar))
async def find_similar(message: types.Message, state: FSMContext):
    mol_smiles = message.text
    if not MyStates.smiles:
        mol_name = mol_smiles
        molecule = new_client.molecule
        response = molecule.filter(
            molecule_synonyms__molecule_synonym__iexact=mol_name
            )
        if response:
            mol_smiles = response[0]['molecule_structures']['canonical_smiles']
        else:
            await message.answer('Ничего не найдено')
    similarity = new_client.similarity
    response = similarity.filter(smiles=mol_smiles, similarity=70)
    if response:
        for molecule in response[:MyStates.count]:
            chembl = molecule['molecule_hierarchy']['molecule_chembl_id']
            mol_smiles = molecule['molecule_structures']['canonical_smiles']
            await message.answer(f'chembl: {chembl}\nsmiles: {mol_smiles}')
    else:
        await message.answer('Ничего не найдено')
    await state.clear()


# @router.message(StateFilter(MyStates.set_count))
# async def set_count(message: types.Message, state: FSMContext):
#     mol_smiles = message.text
#     if not MyStates.smiles:
#         mol_name = mol_smiles
#         molecule = new_client.molecule
#         response = molecule.filter(
#             molecule_synonyms__molecule_synonym__iexact=mol_name
#             )
#         if response:
#             MyStates.data = response[0]['molecule_structures']
#         else:
#             await message.answer('Ничего не найдено')
#     await message.answer(
#         'Введите максимальное число молекул, которое вы хотите получить')
#     await state.set_state(MyStates.choose_type)


# @router.message(StateFilter(MyStates.choose_type))
# async def choose_type(message: types.Message, state: FSMContext):
#     MyStates.count = int(message.text)
#     await message.answer(
#         'В каком виде вы хотите получить молекулы?',
#         reply_markup=Keyboard().choose_type)


# @router.message(F.data == 'chat')
# async def find_similar(message: types.Message, state: FSMContext):
#     mol_smiles = MyStates.data['canonical_smiles']
#     similarity = new_client.similarity
#     response = similarity.filter(smiles=mol_smiles, similarity=70)
#     if response:
#         for molecule in response[:MyStates.count]:
#             chembl = molecule['molecule_hierarchy']['molecule_chembl_id']
#             mol_smiles = molecule['molecule_structures']['canonical_smiles']
#             await message.answer(f'chembl: {chembl}\nsmiles: {mol_smiles}')
#     else:
#         await message.answer('Ничего не найдено')
#     await state.clear()


# @router.callback_query(F.data == 'smi')
# async def make_smi(message: types.Message, state: FSMContext):
#     mol_smiles = MyStates.data['canonical_smiles']
#     similarity = new_client.similarity
#     response = similarity.filter(smiles=mol_smiles, similarity=70)
#     if response:
#         output = ''
#         for molecule in response[:MyStates.count]:
#             print(molecule)
#             if not output:
#                 output = mol_smiles
#             mol_smiles = molecule['molecule_structures']['canonical_smiles']
#             output += message.answer(f'\n{mol_smiles}')
#     else:
#         await message.answer('Ничего не найдено')

#     file = StringIO()
#     file.write(output)
#     file.seek(0)
#     await message.answer_document(
#         types.input_file.BufferedInputFile(
#             BytesIO(file.read().encode('utf-8')).getbuffer(),
#             filename='similar.smi'
#             )
#         )
#     await message.delete()
#     await state.clear()


# @router.callback_query(F.data == 'txt')
# async def find_similar(message: types.Message, state: FSMContext):
#     mol_smiles = MyStates.data['canonical_smiles']
#     similarity = new_client.similarity
#     response = similarity.filter(smiles=mol_smiles, similarity=70)
#     if response:
#         for molecule in response[:MyStates.count]:
#             chembl = molecule['molecule_hierarchy']['molecule_chembl_id']
#             mol_smiles = molecule['molecule_structures']['canonical_smiles']
#             await message.answer(f'chembl: {chembl}\nsmiles: {mol_smiles}')
#     else:
#         await message.answer('Ничего не найдено')
#     await state.clear()
