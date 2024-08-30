import py3Dmol
import pymol
from pymol import cmd
import os

def load_protein(pdb_file_path, width=800, height=600):

    """
    Load a protein structure from a PDB file and display it using py3Dmol.
    pdb_file_path: str, path to the PDB file
    width: int, width of the viewer in pixels
    height: int, height of the viewer in pixels
    return: py3Dmol.view object
    """
    
    with open(pdb_file_path) as ifile:
        pdb_data = "".join([x for x in ifile])
    
    view = py3Dmol.view(width=width, height=height)
    view.addModelsAsFrames(pdb_data)
    
    for line in pdb_data.split("\n"):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM":
            continue
        # Assuming the B-factor is at position 10 (you may need to adjust this based on your PDB format)
        b_factor = float(split[10])
        if b_factor > 90:
            color = "blue"
        elif 70 <= b_factor <= 90:
            color = "cyan"
        elif 50 <= b_factor < 70:
            color = "yellow"
        else:
            color = "orange"
        
        # Atom serial numbers typically start from 1, hence idx should be used directly
        idx = int(split[1])
        
        # Style should be set per atom id
        view.setStyle({'model': -1, 'serial': idx}, {"cartoon": {'color': color}})
    view.zoomTo()
    return view


def align_protein(pred_pdb_file, true_pdb_file, output_dir, pred_color = 'cyan', true_color = 'green', width=800, height=600):
    """
    Align two protein structures and display them using py3Dmol.
    pred_pdb_file: str, path to the PDB file of the predicted protein
    true_pdb_file: str, path to the PDB file of the true protein
    output_dir: str, path to the output directory to save the aligned PDB files
    pred_color: str, color of the predicted protein in the viewer
    true_color: str, color of the true protein in the viewer
    width: int, width of the viewer in pixels
    height: int, height of the viewer in pixels
    return: py3Dmol.view object
    """

    # always reinitialize!
    cmd.reinitialize()

    cmd.load(pred_pdb_file, 'predicted_protein')
    cmd.load(true_pdb_file, 'true_protein')
    
    # Align the structures on the backbone atoms
    cmd.align('predicted_protein & backbone', 'true_protein & backbone', quiet=0)
    
    # Save the aligned structures
    pred_aligned_fp = os.path.join(output_dir, 'aligned_predicted_protein.pdb')
    true_aligned_fp = os.path.join(output_dir, 'aligned_true_protein.pdb')
    cmd.save(pred_aligned_fp, 'predicted_protein')
    cmd.save(true_aligned_fp, 'true_protein')

    # Read PDB files into strings (assuming they are in the current directory)
    with open(pred_aligned_fp, 'r') as file:
        pred_pdb_data = file.read()
    
    with open(true_aligned_fp, 'r') as file:
        true_pdb_data = file.read()
    
    # Create a py3Dmol view
    view = py3Dmol.view(width=width, height=height)
    
    # Add the predicted protein model
    view.addModel(pred_pdb_data, 'pdb')
    # Set a specific color for the predicted protein, e.g., green
    view.setStyle({'model': 0}, {'cartoon': {'color': pred_color}})
    
    # Add the true protein model
    view.addModel(true_pdb_data, 'pdb')
    # Set a different specific color for the true protein, e.g., blue
    view.setStyle({'model': 1}, {'cartoon': {'color': true_color}})

    view.zoomTo()
    return view


