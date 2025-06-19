from chembl_webresource_client.utils import utils
import json
from aiogram import Router, types
from aiogram.filters import Command
from states import MyStates


router = Router()


@router.message(Command('molecular_descriptors'))
async def callback(message: types.Message):
    mol_smiles = MyStates.data['molecule_structures']['canonical_smiles']
    if mol_smiles is None:
        await message.answer('Нет истории поиска молекул')
    else:
        molecule = utils.smiles2ctab(mol_smiles)
        descs = json.loads(utils.chemblDescriptors(molecule))[0]
        response = ''
        for key in descs:
            if not response:
                response = str(f'{key}: {descs[key]}')
            else:
                response += '\n' + str(f'{key}: {descs[key]}')
        await message.answer(response)
