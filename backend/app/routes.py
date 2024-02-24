from flask import Blueprint, request, jsonify
from . import db
from .models import Gene
from .schemas import gene_schema, genes_schema

main = Blueprint('main', __name__)

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