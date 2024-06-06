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

from bs4 import BeautifulSoup


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
        return response.content
    else:
        return None

def fetch_gene_structure(gene_ensembl_id, content_type='application/json'):
    server = "http://rest.ensembl.org"
    exon_endpoint = f"/overlap/id/{gene_ensembl_id}?feature=exon"
    r = requests.get(server + exon_endpoint, headers={"Accept": content_type})

    try:
        r.raise_for_status()
        gene_structure = r.json()
        
        exons = [{'start': exon['start'], 'end': exon['end'], 'Parent': exon['Parent']} for exon in gene_structure]
        return exons
    except requests.exceptions.HTTPError as e:
        print(f"Error fetching gene structure for gene_id {gene_ensembl_id}: {e}")
        return []

@main.route('/run-evo-genes', methods=['POST'])
def run_evo_genes():
    fasta_file1_path = 'temp_sequence1.fasta'
    fasta_file2_path = 'temp_sequence2.fasta'

    if 'GeneID1' in request.form and 'GeneID2' in request.form:
        gene_id1 = request.form['GeneID1']
        gene_id2 = request.form['GeneID2']
    
        sequence1 = fetch_sequence_from_ensembl(gene_id1)
        sequence2 = fetch_sequence_from_ensembl(gene_id2)
        
        if sequence1 and sequence2:
            with open(fasta_file1_path, 'wb') as file1, open(fasta_file2_path, 'wb') as file2:
                file1.write(sequence1)
                file2.write(sequence2)
        else:
            return jsonify({'error': 'Failed to fetch sequences from Ensembl.'}), 400

    yass_output_path = 'yass_output.yop'
    dp_output_path = 'dp.png'
    yass_executable = './yass-Win64.exe'
    command = [yass_executable, fasta_file1_path, fasta_file2_path, '-o', yass_output_path]
    subprocess.run(command, check=True)
    
    python_executable = 'python'
    yop_reader_script = 'yop_reader.py'
    command = [python_executable, yop_reader_script, yass_output_path, dp_output_path]
    subprocess.run(command, check=True)

    with open(dp_output_path, 'rb') as file:
        dotplot_image_data = file.read()

    gene_structure1 = fetch_gene_structure(gene_id1)
    gene_structure2 = fetch_gene_structure(gene_id2)

    exon_intervals1 = {parent: [(exon['start'], exon['end']) for exon in gene_structure1 if exon['Parent'] == parent] for parent in set(exon['Parent'] for exon in gene_structure1)}
    exon_intervals2 = {parent: [(exon['start'], exon['end']) for exon in gene_structure2 if exon['Parent'] == parent] for parent in set(exon['Parent'] for exon in gene_structure2)}

    # Return the raw data along with HTML
    gene_structure1_html = create_gene_plot(exon_intervals1[list(exon_intervals1.keys())[0]]).to_html()
    gene_structure2_html = create_gene_plot(exon_intervals2[list(exon_intervals2.keys())[0]]).to_html()

    soup1 = BeautifulSoup(gene_structure1_html, 'html.parser')
    gene_structure1_body = soup1.body.decode_contents()
    soup2 = BeautifulSoup(gene_structure2_html, 'html.parser')
    gene_structure2_body = soup2.body.decode_contents()

    os.remove(fasta_file1_path)
    os.remove(fasta_file2_path)
    os.remove(yass_output_path)
    os.remove(dp_output_path)
    
    return jsonify({
        'dotplot_image': dotplot_image_data.decode('latin1'),
        'gene_structure1_html': gene_structure1_body,
        'gene_structure2_html': gene_structure2_body,
        'exon_intervals1': exon_intervals1,
        'exon_intervals2': exon_intervals2
    })



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


# def fetch_gene_structure(gene_ensembl_id, content_type='application/json'):
#     server = "http://rest.ensembl.org"
#     exon_endpoint = f"/overlap/id/{gene_ensembl_id}?feature=exon"
#     r = requests.get(server + exon_endpoint, headers={"Accept": content_type})

#     try:
#         r.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
#         gene_structure = r.json()  # Parse JSON response
#         return gene_structure
#     except requests.exceptions.HTTPError as e:
#         logging.error(f"Error fetching gene structure for gene_id {gene_ensembl_id}: {e}")
#         return None  # Return None to indicate failure
    

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