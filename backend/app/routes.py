from flask import Blueprint, request, jsonify, render_template, Flask,send_file,current_app,send_from_directory,Response
# from . import db
from .models import Gene
from .schemas import gene_schema, genes_schema
import requests, sys, json
import logging

from flask_cors import CORS,cross_origin
import os
from .dash_app import create_dash_app

from .extensions import db  # Make sure this import is correct based on your setup
from .GeneImage import GeneImage  # Import the GeneImage class

import subprocess
import tempfile
import io  
import re

app = Flask(__name__)
CORS(app, supports_credentials=True, allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "OPTIONS"])

dash_app, create_gene_plot = create_dash_app(app)


#Blueprints
main = Blueprint('main', __name__)
generate = Blueprint('generate', __name__)
@generate.route('/test', methods=['GET'])
def test():
    return "Blueprint is working!"

@main.route('/', methods=['GET'])
def get_data():
    return jsonify({"Hello": "World"})



UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'backend')



def fetch_sequence_from_ensembl(gene_id):
    ensembl_url = f'https://rest.ensembl.org/sequence/id/{gene_id}?content-type=text/x-fasta'
    response = requests.get(ensembl_url)
    if response.ok:
        # Extract the sequence part from the FASTA content
        fasta_content = response.text
        sequence_lines = fasta_content.split('\n')[1:]  # Skip the FASTA header
        sequence = ''.join(sequence_lines)  # Join lines to form the full sequence
        return sequence
    else:
        return None


@main.route('/run-yass', methods=['POST'])
def run_yass():
    #to show the real output of yass you need to comment this lines.
    # image_directory = '../'  # This navigates up from 'backend/app' to 'backend'
    # image_filename = 'example.png'
    # try:
    #     return send_from_directory(image_directory, image_filename)
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500

    fasta_file1_path = 'temp_sequence1.fasta'
    fasta_file2_path = 'temp_sequence2.fasta'

    if 'fasta1' in request.files and 'fasta2' in request.files:
        fasta_file1 = request.files['fasta1']
        fasta_file2 = request.files['fasta2']
        fasta_file1.save(fasta_file1_path)
        fasta_file2.save(fasta_file2_path)
    elif 'sequence1' in request.form and 'sequence2' in request.form:
        sequence1 = request.form['sequence1']
        sequence2 = request.form['sequence2']
        # Validate sequence input
        if not re.match('^[ACGTacgt]*$', sequence1) or not re.match('^[ACGTacgt]*$', sequence2):
            return jsonify({'error': 'Invalid sequence input. Sequences should only contain A, C, G, T characters.'}), 400
        with open(fasta_file1_path, 'w') as file1, open(fasta_file2_path, 'w') as file2:
            file1.write(f'>Sequence1\n{sequence1}\n')
            file2.write(f'>Sequence2\n{sequence2}\n')
    elif 'GeneID1' in request.form and 'GeneID2' in request.form:
        gene_id1 = request.form['GeneID1']
        gene_id2 = request.form['GeneID2']
        
        # Fetch sequences corresponding to GeneIDs from Ensembl API
        sequence1 = fetch_sequence_from_ensembl(gene_id1)
        sequence2 = fetch_sequence_from_ensembl(gene_id2)

        # Validate sequence input
        if not sequence1 or not sequence2:
            return jsonify({'error': 'Failed to fetch sequences from Ensembl. Please check the GeneID inputs.'}), 400
        if not re.match('^[ACGTacgt]*$', sequence1) or not re.match('^[ACGTacgt]*$', sequence2):
            return jsonify({'error': 'Invalid sequence input. Sequences should only contain A, C, G, T characters.'}), 400
        with open(fasta_file1_path, 'w') as file1, open(fasta_file2_path, 'w') as file2:
            file1.write(f'>Sequence1\n{sequence1}\n')
            file2.write(f'>Sequence2\n{sequence2}\n')

    else:
        return jsonify({'error': 'No valid sequence or file input provided'}), 400



    # Proceed with YASS processing if inputs are valid
    yass_output_path = 'yass_output.yop'
    dp_output_path = 'dp.png'
    yass_executable ='./yass-Win64.exe'
    command = [yass_executable, fasta_file1_path, fasta_file2_path, '-o', yass_output_path]
    subprocess.run(command, check=True)
    
    # php_script = 'yass2dotplot.php'
    # subprocess.run(['php', php_script, yass_output_path, dp_output_path], check=True)
    

    python_executable = 'python'
    # python_executable = os.path.join(os.environ['VIRTUAL_ENV'], 'Scripts', 'python.exe')  # For Windows
    yop_reader_script = 'yop_reader.py'

    # yop_reader_script = os.getcwd()+'\\backend\\yop_reader.py'

    # yop_reader_script = os.path.join(os.getcwd(), 'backend', 'yop_reader.py')


    command = [python_executable, yop_reader_script, yass_output_path, dp_output_path]
    subprocess.run(command, check=True)

    with open(dp_output_path, 'rb') as file:
        image_data = file.read()
    
    os.remove(fasta_file1_path)
    os.remove(fasta_file2_path)
    os.remove(yass_output_path)
    os.remove(dp_output_path)
    
    return Response(image_data, mimetype='image/png')




@main.route('/add', methods=['POST'])
def add_gene():
    data = request.get_json()

    # Check if the request JSON contains 'gene_name' and 'sequence'
    if not data or 'gene_name' not in data or 'sequence' not in data:
        return jsonify({"error": "Missing gene_name or sequence"}), 400

    # Create a new Gene object with the data
    new_gene = Gene(gene_name=data['gene_name'], sequence=data['sequence'])

    # Add the new Gene object to the session and commit it to the database
    db.session.add(new_gene)
    db.session.commit()

    # Return a response indicating success, including the added gene's ID
    return jsonify({"message": "Gene added successfully", "gene_id": new_gene.id}), 201




@main.route('/genes', methods=['GET'])
def get_genes():
    # Query all gene records from the database
    all_genes = Gene.query.all()
    # Serialize the list of gene records to JSON
    result = genes_schema.dump(all_genes)
    # Return the serialized gene records as JSON
    return jsonify(result)

@generate.route('/generate', methods=['POST'])
def run_generate():
    data = request.get_json()
    sequence1 = data.get('sequence1', '')
    sequence2 = data.get('sequence2', '')

    # Implementation of the YASS algorithm logic here
    # ...

    # For now, return a placeholder response
    return jsonify({"message": "Graph generated successfully"})

@generate.route('/get-gene-seq', methods=['POST'])
def get_gene_seq():
    data = request.get_json()
    gene_id = data.get('gene_id', '')

    if not gene_id:
        return jsonify({"error": "Missing gene_id"}), 400

    content_type = 'application/json'
    x_fasta_content = fetch_endpoint(gene_id, content_type)

    return jsonify({"x_fasta_content": x_fasta_content})

def fetch_endpoint(gene_ensembl_id, content_type):
    server = "http://rest.ensembl.org/"
    request = f"/sequence/id/{gene_ensembl_id}?"
    r = requests.get(server + request, headers={"Accept": content_type})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    return r.json()

@generate.route('/gene-structure', methods=['POST'])
@cross_origin()
def get_gene_structure():
    data = request.get_json()
    gene_id = data.get('gene_id', '')

    if not gene_id:
        logging.error("Missing gene_id in get_gene_structure route")
        return jsonify({"error": "Missing gene_id"}), 400

    logging.info(f"Fetching gene structure for gene_id: {gene_id}")
    gene_structure = fetch_gene_structure(gene_id)
    return jsonify(gene_structure)


def fetch_gene_structure(gene_ensembl_id, content_type='application/json'):
    server = "http://rest.ensembl.org"
    exon_endpoint = f"/overlap/id/{gene_ensembl_id}?feature=exon"
    r = requests.get(server + exon_endpoint, headers={"Accept": content_type})

    try:
        r.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        gene_structure = r.json()  # Parse JSON response
        return gene_structure
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error fetching gene structure for gene_id {gene_ensembl_id}: {e}")
        return None  # Return None to indicate failure
    

@generate.route('/gene-image', methods=['POST'])
@cross_origin()
def plot_gene_image():
    data = request.json
    exons_positions = data.get('exonsPositions', [])
    
    if not exons_positions:
        return jsonify({"error": "No exon positions provided"}), 400

    # Generate the Plotly figure using the provided exon positions
    figure = create_gene_plot(exons_positions[0])

    # Return the HTML representation of the figure
    return Response(figure.to_html(), content_type='text/html')

# Define the update and plot endpoints
@main.route('/dash/update', methods=['POST'])
def update_exon_positions():
    data = request.json
    exons_positions = data.get('exonsPositions', [])
    return jsonify(success=True)

@main.route('/dash/plot', methods=['GET'])
def plot_gene_structure():
    positions = request.args.get('positions')
    exons_positions = json.loads(positions) if positions else []
    fig = create_gene_plot(exons_positions)
    return fig.to_html()