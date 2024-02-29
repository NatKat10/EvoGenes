from flask import Blueprint, request, jsonify, render_template, Flask
from . import db
from .models import Gene
from .schemas import gene_schema, genes_schema
import requests, sys, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "OPTIONS"])

#Blueprints
main = Blueprint('main', __name__)
generate = Blueprint('generate', __name__)

@main.route('/', methods=['GET'])
def get_data():
    return jsonify({"Hello": "World"})

@main.route('/add', methods=['POST'])
def add_gene():
    data = request.get_json()
    if not data or 'gene_name' not in data or 'sequence' not in data:
        return jsonify({"error": "Missing gene_name or sequence"}), 400
    
    new_gene = Gene(gene_name=data['gene_name'], sequence=data['sequence'])
    db.session.add(new_gene)
    db.session.commit()
    return gene_schema.jsonify(new_gene), 201


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
