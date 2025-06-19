from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from chembl_webresource_client.new_client import new_client
from aiogram.fsm.context import FSMContext
from states import MyStates
from .keyboard import Keyboard
from CGRtools import SDFWrite, smiles
from io import StringIO, BytesIO


router = Router()


@router.message(Command('get_smiles'))
async def get_smiles(message: types.Message):
    print('\n', type(Keyboard().smiles), Keyboard().smiles, '\n')
    await message.answer('Выберите тип поиска',
                         reply_markup=Keyboard().smiles)


@router.message(F.text == 'По названию')
async def name(message: types.Message, state: FSMContext):
    await message.answer(
        'Введите название молекулы (на английском)',
        reply_markup=types.ReplyKeyboardRemove()
        )
    await state.set_state(MyStates.wait_name)


@router.message(StateFilter(MyStates.wait_name))
async def name_find(message: types.Message, state: FSMContext):
    mol_name = message.text
    molecule = new_client.molecule
    response = molecule.filter(
        molecule_synonyms__molecule_synonym__iexact=mol_name
        )
    if response:
        mol_smiles = response[0]['molecule_structures']['canonical_smiles']
        MyStates.data = response[0]
        await message.answer(f'{mol_smiles}\n\nДругие форматы:',
                             reply_markup=Keyboard().select_type)
    else:
        await message.answer('Ничего не найдено')
    await state.clear()


@router.message(F.text == 'По CHEMBL ID')
async def chembl_id(message: types.Message, state: FSMContext):
    await message.answer(
        'Введите CHEMBL ID',
        reply_markup=types.ReplyKeyboardRemove()
        )
    await state.set_state(MyStates.wait_chembl_id)


@router.message(StateFilter(MyStates.wait_chembl_id))
async def chembl_find(message: types.Message, state: FSMContext):
    mol_id = message.text
    if not mol_id.startswith('CHEMBL'):
        mol_id = 'CHEMBL' + mol_id
    molecule = new_client.molecule
    response = molecule.filter(chembl_id=mol_id)
    if response:
        mol_smiles = response[0]['molecule_structures']['canonical_smiles']
        MyStates.data = response[0]
        await message.answer(f'{mol_smiles}\n\nДругие форматы:',
                             reply_markup=Keyboard().select_type)
    else:
        await message.answer('Ничего не найдено')
    await state.clear()


@router.message(F.text == 'По INCHI')
async def inchi(message: types.Message, state: FSMContext):
    await message.answer(
        'Введите INCHI',
        reply_markup=types.ReplyKeyboardRemove()
        )
    await state.set_state(MyStates.wait_inchi)


@router.message(StateFilter(MyStates.wait_inchi))
async def inchi_find(message: types.Message, state: FSMContext):
    mol_inchi = message.text
    molecule = new_client.molecule
    response = molecule.filter(
        molecule_structures__standard_inchi_key=mol_inchi
        )
    if response:
        mol_smiles = response[0]['molecule_structures']['canonical_smiles']
        MyStates.data = response[0]
        await message.answer(f'{mol_smiles}\n\nДругие форматы:',
                             reply_markup=Keyboard().select_type)
    else:
        await message.answer('Ничего не найдено')
    await state.clear()


@router.callback_query(F.data == 'sdf')
async def get_sdf(callback: types.CallbackQuery, state: FSMContext):
    molecule = MyStates.data
    mol_smiles = molecule['molecule_structures']['canonical_smiles']
    chembl_id = molecule['molecule_hierarchy']['molecule_chembl_id']
    file = StringIO()
    with SDFWrite(file) as f:
        f.write(smiles(mol_smiles))
        file.seek(0)

    await callback.message.answer_document(
        types.input_file.BufferedInputFile(
            BytesIO(file.read().encode('utf-8')).getbuffer(),
            filename=f'{chembl_id}.sdf'
            )
        )
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data == 'smi')
async def get_smi(callback: types.CallbackQuery, state: FSMContext):
    molecule = MyStates.data
    mol_smiles = molecule['molecule_structures']['canonical_smiles']
    chembl_id = molecule['molecule_hierarchy']['molecule_chembl_id']
    file = StringIO()
    file.write(mol_smiles)
    file.seek(0)
    await callback.message.answer_document(
        types.input_file.BufferedInputFile(
            BytesIO(file.read().encode('utf-8')).getbuffer(),
            filename=f'{chembl_id}.smi'
            )
        )

    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data == 'png')  #redo
async def get_png(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('В разработке')
    await callback.answer()
    # molecule = MyStates.data
    # print(molecule)
    # mol_smiles = molecule['molecule_structures']['canonical_smiles']
    # chembl_id = molecule['molecule_hierarchy']['molecule_chembl_id']
    # file = StringIO()
    # with SDFWrite(file) as f:
    #     f.write(smiles(CGRContainer.depict(mol_smiles)))
    #     file.seek(0)

    # await callback.message.answer_document(
    #     types.input_file.BufferedInputFile(
    #         BytesIO(file.read().encode('utf-8')).getbuffer(),
    #         filename=f'{chembl_id}.png'
    #         )
    #     )
    # await callback.message.delete()
    # await callback.answer()
