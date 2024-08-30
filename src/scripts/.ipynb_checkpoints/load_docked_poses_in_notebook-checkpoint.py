import py3Dmol
import os
import json

def ansi_color(text, color):
    """Color text for console output"""
    colors = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m"
    }
    return f"{colors[color]}{text}{colors['reset']}"

def show_docked_poses(protein_path, protein_name, ligands_directory, width = 800, height = 600):
    """
    Show the docked protein and ligand structures using Py3Dmol
    protein_path: str, path to the protein file
    protein_name: str, name of the protein
    ligands_directory: str, path to the directory containing ligand files and output.json
    width: int, width of the viewer
    height: int, height of the viewer
    return: py3Dmol.view object
    """
    # Create a viewer object from Py3Dmol
    viewer = py3Dmol.view(width=width, height=height)

    # Load the protein structure
    with open(protein_path, 'r') as protein_file:
        protein_data = protein_file.read()
    viewer.addModel(protein_data, protein_name)
    viewer.setStyle({'cartoon': {'color': 'green'}})

    # Load confidence scores from output.json
    output_json_path = os.path.join(ligands_directory, 'output.json')
    with open(output_json_path, 'r') as file:
        data = json.load(file)
        confidence_scores = np.array(data['position_confidence']).flatten() # list of floats

    # Load all ligand files from the directory and match with confidence scores
    ligand_files = [f for f in os.listdir(diffdock_output_dir) if f.endswith('.sdf')]
    ligand_files.sort(key=lambda x: (int(x.split('_')[1]), int(x.split('_')[3].split('.')[0])))

    for index, file in enumerate(ligand_files):
        ligand_path = os.path.join(ligands_directory, file)
        with open(ligand_path, 'r') as ligand_file:
            ligand_data = ligand_file.read()
        ligand_name = file.split('.')[0]
        viewer.addModel(ligand_data, 'sdf')
        score = round(confidence_scores[index], 3)
        score_color = "green" if score > 0.5 else "blue" if score >= -1.5 else "red"
        viewer.setStyle({'model': index + 1}, {'stick': {'radius': 0.3}})
        print(f"Loaded {ansi_color(ligand_name, 'yellow')} with confidence score: {ansi_color(score, score_color)}")

    # Zoom to the complex and render
    viewer.zoomTo()
    return viewer