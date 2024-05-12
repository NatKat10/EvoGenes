from flask import Blueprint, request, jsonify, render_template, Flask
# from . import db
from .models import Gene
from .schemas import gene_schema, genes_schema
# import requests, sys, json
import requests, sys, json
import logging

from flask_cors import CORS
from flask_cors import cross_origin


app = Flask(__name__)
CORS(app, supports_credentials=True, allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "OPTIONS"])

#Blueprints
main = Blueprint('main', __name__)
generate = Blueprint('generate', __name__)
@generate.route('/test', methods=['GET'])
def test():
    return "Blueprint is working!"

@main.route('/', methods=['GET'])
def get_data():
    return jsonify({"Hello": "World"})

import os
from flask import send_file,send_from_directory

from flask import jsonify, request,send_file,current_app
from .extensions import db  # Make sure this import is correct based on your setup
from .models import Gene  # Adjust this import if necessary

from .GeneImage import GeneImage  # Import the GeneImage class

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'backend')

import subprocess
import os
import tempfile
from flask import Response
import io  
import re







@main.route('/run-yass', methods=['POST'])
def run_yass():
        # Uncomment this block to serve an example image instead of processing the sequences
    image_directory = '../'  # This navigates up from 'backend/app' to 'backend'
    image_filename = 'example.png'
    return send_from_directory(image_directory, image_filename)

    # fasta_file1_path = 'temp_sequence1.fasta'
    # fasta_file2_path = 'temp_sequence2.fasta'

    # if 'fasta1' in request.files and 'fasta2' in request.files:
    #     fasta_file1 = request.files['fasta1']
    #     fasta_file2 = request.files['fasta2']
    #     fasta_file1.save(fasta_file1_path)
    #     fasta_file2.save(fasta_file2_path)
    # elif 'sequence1' in request.form and 'sequence2' in request.form:
    #     sequence1 = request.form['sequence1']
    #     sequence2 = request.form['sequence2']
    #     # Validate sequence input
    #     if not re.match('^[ACGTacgt]*$', sequence1) or not re.match('^[ACGTacgt]*$', sequence2):
    #         return jsonify({'error': 'Invalid sequence input. Sequences should only contain A, C, G, T characters.'}), 400
    #     with open(fasta_file1_path, 'w') as file1, open(fasta_file2_path, 'w') as file2:
    #         file1.write(f'>Sequence1\n{sequence1}\n')
    #         file2.write(f'>Sequence2\n{sequence2}\n')
    # else:
    #     return jsonify({'error': 'No valid sequence or file input provided'}), 400



    # # Proceed with YASS processing if inputs are valid
    # yass_output_path = 'yass_output.yop'
    # dp_output_path = 'dp.png'
    # yass_executable = './yass-Win64.exe'
    # command = [yass_executable, fasta_file1_path, fasta_file2_path, '-o', yass_output_path]
    # subprocess.run(command, check=True)
    
    # php_script = 'yass2dotplot.php'
    # subprocess.run(['php', php_script, yass_output_path, dp_output_path], check=True)
    
    # with open(dp_output_path, 'rb') as file:
    #     image_data = file.read()
    
    # os.remove(fasta_file1_path)
    # os.remove(fasta_file2_path)
    # os.remove(yass_output_path)
    # os.remove(dp_output_path)
    
    # return Response(image_data, mimetype='image/png')


    # code for file input only
    # fasta_file1 = request.files['fasta1']
    # fasta_file2 = request.files['fasta2']
    
    # # Save files to temporary paths
    # fasta_file1_path = 'temp_sequence1.fasta'
    # fasta_file2_path = 'temp_sequence2.fasta'
    # fasta_file1.save(fasta_file1_path)
    # fasta_file2.save(fasta_file2_path)
    
    # # Define output paths
    # yass_output_path = 'yass_output.yop'
    # dp_output_path = 'dp.png'
    
    # # Run YASS with the FASTA files
    # yass_executable = './yass-Win64.exe'
    # command = [yass_executable, fasta_file1_path, fasta_file2_path, '-o', yass_output_path]
    # subprocess.run(command, check=True)
    
    # # Convert YOP to DotPlot
    # php_script = 'yass2dotplot.php'  # Make sure this script is executable and has a .php extension
    # subprocess.run(['php', php_script, yass_output_path, 'filename1="gene1"', 'filename2="gene2"', dp_output_path], check=True)
    
    # # Send the DotPlot image file as a response
    # with open(dp_output_path, 'rb') as file:
    #     image_data = file.read()
    
    # # Delete temporary files
    # os.remove(fasta_file1_path)
    # os.remove(fasta_file2_path)
    # os.remove(yass_output_path)
    # os.remove(dp_output_path)
    
    # return Response(image_data, mimetype='image/png')


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
    
    # Generate the gene image plot
    gene = GeneImage(exons_positions, exons_positions[0])

    # Ensure the directory exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    image_path = os.path.join(UPLOAD_FOLDER, 'gene_image.png')
    gene.save_plot(image_path)  # Save the image file
    
    # Return the image file as a response
    return send_file(image_path, mimetype='image/png')