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


from flask import jsonify, request

from flask import jsonify, request
from .extensions import db  # Make sure this import is correct based on your setup
from .models import Gene  # Adjust this import if necessary

from .GeneImage import GeneImage  # Import the GeneImage class


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
    gene = GeneImage(exons_positions,exons_positions[0])
    gene.save_plot()  # Adjust the output path as needed

    return jsonify({'message': 'Gene image plot generated successfully'})