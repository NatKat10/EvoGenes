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

import subprocess
import tempfile
import io  
import re

from bs4 import BeautifulSoup
from yop_reader import process_sequences



app = Flask(__name__)
CORS(app, supports_credentials=True, allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "OPTIONS"])

dash_app, create_gene_plot, plot_dotplot = create_dash_app(app)


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
    ensembl_url = f'https://rest.ensembl.org/sequence/id/{gene_id}?content-type=text/x-fasta'#string for the api request
    response = requests.get(ensembl_url)#api request to ensembl website to get the sequance of the gene in fasta file
    if response.ok:# check if we got status 200 from the request
        sequence = response.content.decode('utf-8')#decode from bytes to utf-8
        gene_id_extracted = sequence.split('\n', 1)[0].split()[0].lstrip('>')
        #sequence.split('\n', 1)[0]- the header line of the fasta 
        #split()[0]- split the header to words and take the first one
        #lstrip('>')- remove the > char from the gene id
        return sequence.encode('utf-8'), gene_id_extracted# encode back to bytes and return, return gene id for the label
    else:
        return None, None

def fetch_gene_structure(gene_ensembl_id, content_type='application/json'):
    server = "http://rest.ensembl.org"# base url of ensembl REST API server
    exon_endpoint = f"/overlap/id/{gene_ensembl_id}?feature=exon"# add to base url to get the gene structures from ensembl
    r = requests.get(server + exon_endpoint, headers={"Accept": content_type})#sent api request

    try:
        r.raise_for_status()# raises httpError if status code is more then 400
        gene_structure = r.json()
        
        exons = [{'start': exon['start'], 'end': exon['end'], 'Parent': exon['Parent']} for exon in gene_structure]
        # creates a list of dictionaries containing the start and end position for each
        #exon and its parent gene.
        return exons#Returns the list of dictionaries containing the extracted exon information
    except requests.exceptions.HTTPError as e:
        print(f"Error fetching gene structure for gene_id {gene_ensembl_id}: {e}")#raise error if there is httpError
        return []

@main.route('/run-evo-genes', methods=['POST'])

def run_evo_genes():
    fasta_file1_path = 'temp_sequence1.fasta'#temporary fsta files to input to yass
    fasta_file2_path = 'temp_sequence2.fasta'

    if 'GeneID1' in request.form and 'GeneID2' in request.form:
        #checks if form data contains gene 1 and gene 2
        gene_id1 = request.form['GeneID1']#extract the gene IDs from the form data
        gene_id2 = request.form['GeneID2']
    
        sequence1, extracted_gene_id1 = fetch_sequence_from_ensembl(gene_id1)
        sequence2, extracted_gene_id2 = fetch_sequence_from_ensembl(gene_id2)
        # fetch the sequence for the given gene IDs
        
        if sequence1 and sequence2:
            #If both sequences are successfully fetched, they are written to the temporary FASTA files.
            with open(fasta_file1_path, 'wb') as file1, open(fasta_file2_path, 'wb') as file2:
                file1.write(sequence1)
                file2.write(sequence2)
        else:
            return jsonify({'error': 'Failed to fetch sequences from Ensembl.'}), 400

    yass_output_path = 'yass_output.yop'#save yass output to file
    yass_executable = './yass-Win64.exe'
    command = [yass_executable, fasta_file1_path, fasta_file2_path, '-o', yass_output_path]#create yass command line 
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)#run yass with the command line
    yass_output = result.stdout + result.stderr

    result_sequences, directions, min_x, max_x, min_y, max_y, _, _ = process_sequences(yass_output_path)
    #calls the process_sequences function to process the YASS output file and extract the necessary data for visualization.


    gene_structure1 = fetch_gene_structure(gene_id1)
    gene_structure2 = fetch_gene_structure(gene_id2)
    #fetch the exon structures for the given gene IDs

    exon_intervals1 = {parent: [(exon['start'], exon['end']) for exon in gene_structure1 if exon['Parent'] == parent] for parent in set(exon['Parent'] for exon in gene_structure1)}
    exon_intervals2 = {parent: [(exon['start'], exon['end']) for exon in gene_structure2 if exon['Parent'] == parent] for parent in set(exon['Parent'] for exon in gene_structure2)}
    # transform the list of exons into dictionaries where the keys are parent gene IDs, and the values are lists of tuples representing the start and end positions of the exons.


    # Normalize gene structure coordinates to dot plot range
    def normalize_exons(exon_intervals, min_val, max_val):
        # exon_intervals is a dictionary where the keys are parent IDs
        # and the values are lists of tuples representing the start and end positions of exons
        normalized_intervals = {}
        for parent, intervals in exon_intervals.items():
            min_start = min(start for start, end in intervals)#choose the minimum start value across all exons for this parent
            max_end = max(end for start, end in intervals)#choose the maximum end value across all exons for this parent
            gene_length = max_end - min_start# calculate the lenght of the gene 
            normalized_intervals[parent] = [(min_val + ((start - min_start) / gene_length) * (max_val - min_val),# a formula for normalization 
                                             min_val + ((end - min_start) / gene_length) * (max_val - min_val)) for start, end in intervals]
            #for example - Original range: 2,000,000 to 2,002,000 (gene structure), Target range: 1 to 2001 (dot plot)
            #For an exon from 2,000,000 to 2,000,500 - the interval [2,000,000, 2,000,500] in the gene structure maps to [1, 501] in the dot plot.
        return normalized_intervals

    normalized_exons1 = normalize_exons(exon_intervals1, min_x, max_x)
    #normalize gene 1 to fit with the x-axis range of the dotplot
    normalized_exons2 = normalize_exons(exon_intervals2, min_y, max_y)
    #normalize gene 2 to fit with the y-axis range of the dotplot


    gene_structure1_html = create_gene_plot(normalized_exons1[list(normalized_exons1.keys())[0]], x_range=[min_x, max_x]).to_html()
    #Generate the gene structure plot for gene1 and convert it to HTML.
    gene_structure2_html = create_gene_plot(normalized_exons2[list(normalized_exons2.keys())[0]], x_range=[min_y, max_y]).to_html()
    #Generate the gene structure plot for gene2 and convert it to HTML.

    soup1 = BeautifulSoup(gene_structure1_html, 'html.parser')
    #parse the HTML content and extract the body content of the two genes
    gene_structure1_body = soup1.body.decode_contents()
    soup2 = BeautifulSoup(gene_structure2_html, 'html.parser')
    gene_structure2_body = soup2.body.decode_contents()

    os.remove(fasta_file1_path)
    os.remove(fasta_file2_path)
    os.remove(yass_output_path)

    dotplot_data = {#Create a dictionary to store the necessary data for generating the dot plot.
        'directions': directions,
        'min_x': min_x,
        'max_x': max_x,
        'min_y': min_y,
        'max_y': max_y,
        'x_label': extracted_gene_id1,  # Use only the gene ID for label
        'y_label': extracted_gene_id2   # Use only the gene ID for label
    }

    return jsonify({#Return the collected data as a JSON response.
        'dotplot_data': dotplot_data,#The data needed to create the dot plot.
        'gene_structure1_html': gene_structure1_body,#The HTML content for gene1's structure.
        'gene_structure2_html': gene_structure2_body,#The HTML content for gene2's structure.
        'exon_intervals1': normalized_exons1,#The normalized exon intervals for gene1.
        'exon_intervals2': normalized_exons2,#The normalized exon intervals for gene2.
        'yass_output': yass_output#The output from the YASS alignment that shown in a "?"
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

    

@generate.route('/gene-image', methods=['POST'])
@cross_origin()
def plot_gene_image():
    data = request.json #Extracts JSON data from the request.
    exons_positions = data.get('exonsPositions', [])# Retrieves the exon positions from the JSON data.
    
    if not exons_positions:
        return jsonify({"error": "No exon positions provided"}), 400

    # Generate the Plotly figure using the provided exon positions
    figure = create_gene_plot(exons_positions[0])

    # Return the HTML representation of the figure
    return Response(figure.to_html(), content_type='text/html')

# Define the update and plot endpoints
@main.route('/dash/update', methods=['POST'])#This route handles POST requests to update exon positions data
def update_exon_positions():
    data = request.json
    exons_positions = data.get('exonsPositions', [])
    return jsonify(success=True)

@main.route('/dash/plot', methods=['GET'])#This route handles GET requests to generate and return the HTML representation of a gene structure plot based on provided exon positions.
def plot_gene_structure():
    positions = request.args.get('positions')#Retrieves the positions parameter from the query string.
    exons_positions = json.loads(positions) if positions else []#Parses the positions parameter from JSON format to a Python list.
    fig = create_gene_plot(exons_positions)#Calls create_gene_plot to generate the Plotly figure using the provided exon position
    return fig.to_html()


@main.route('/dash/dotplot/update', methods=['POST'])
def update_dotplot_data():#This route handles POST requests to update dot plot data.
    data = request.json
    dotplot_data = data.get('dotplot_data', {})# Retrieves the dot plot data from the JSON data.
    return jsonify(success=True)

@main.route('/dash/dotplot/plot', methods=['POST'])
def plot_dotplot_route():
    dotplot_data = request.json['dotplot_data']#Extracts the dot plot data from the JSON request.
    fig = plot_dotplot(dotplot_data['directions'],#Calls plot_dotplot to generate the Plotly figure using the provided dot plot data.
                       dotplot_data['min_x'], dotplot_data['max_x'],
                       dotplot_data['min_y'], dotplot_data['max_y'],
                       dotplot_data['x_label'], dotplot_data['y_label'])
    return fig.to_html()