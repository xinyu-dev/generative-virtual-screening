
from rdkit.Chem import AllChem
from rdkit import Chem


def convert_mols_to_canonical_smiles(mol_list):
    """
    Convert mol objects to canonical SMILES, and remove duplicates
    :param mol_list: list of mol objects
    :return: list of canonical SMILES
    """
    canonical_smiles = set()
    for mol in mol_list:
        canonical_smi = Chem.MolToSmiles(mol, canonical=True)
        canonical_smiles.add(canonical_smi)
    return list(canonical_smiles)


def convert_smiles_to_sdf(smiles_list, output_dir):
    """
    Convert SMILES to SDF
    :param smiles_list: list of smiles
    :param output_dir: str, output directory
    :return: list of canonical smiles strings
    """
    
    # convert to mol
    mol_list = [Chem.MolFromSmiles(smiles, sanitize=True) for smiles in smiles_list]

    # convert to canonical smiles
    valid_canonical_smiles = convert_mols_to_canonical_smiles(mol_list=mol_list)

    if len(valid_canonical_smiles) < len(mol_list):
        print("Some SMILES are duplicates and removed")

    # convert to SDF
    output_files = []
    for i, smiles in enumerate(valid_canonical_smiles):
        mol = Chem.MolFromSmiles(smiles)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol)
        AllChem.UFFOptimizeMolecule(mol)

        # save the clean file to molmim_result

        w = Chem.SDWriter(f"{output_dir}/molecule_{i}.sdf")
        w.write(mol)
        w.close()
        print(f"Converted SMILES to SDF: {smiles}")
        output_files.append(f"{output_dir}/molecule_{i}.sdf")

    return valid_canonical_smiles
