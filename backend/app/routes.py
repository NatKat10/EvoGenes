from flask import Blueprint, request, jsonify, Flask
from .models import GeneComparison
from .extensions import db
import requests
import subprocess
import os
import json
from .dash_app import create_dash_app
from yop_reader import process_sequences
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "OPTIONS"])

dash_app, create_gene_plot, plot_dotplot = create_dash_app(app)

main = Blueprint('main', __name__)
generate = Blueprint('generate', __name__)

def fetch_sequence_from_ensembl(gene_id):
    ensembl_url = f'https://rest.ensembl.org/sequence/id/{gene_id}?content-type=text/x-fasta'
    response = requests.get(ensembl_url)
    if response.ok:
        sequence = response.content.decode('utf-8')
        gene_id_extracted = sequence.split('\n', 1)[0].split()[0].lstrip('>')
        return sequence.encode('utf-8'), gene_id_extracted
    else:
        return None, None

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
    if 'GeneID1' in request.form and 'GeneID2' in request.form:
        gene_id1 = request.form['GeneID1']
        gene_id2 = request.form['GeneID2']

        # Ensure the gene IDs are always ordered for consistency
        gene_id1, gene_id2 = sorted([gene_id1, gene_id2])

        # Check if the comparison already exists in the database
        comparison = GeneComparison.query.filter(
            ((GeneComparison.gene_id1 == gene_id1) & (GeneComparison.gene_id2 == gene_id2)) |
            ((GeneComparison.gene_id1 == gene_id2) & (GeneComparison.gene_id2 == gene_id1))
        ).first()

        if comparison:
            # Return the existing comparison data
            return jsonify({
                'dotplot_data': json.loads(comparison.dotplot_data),
                'gene_structure1_html': comparison.gene_structure1_html,
                'gene_structure2_html': comparison.gene_structure2_html,
                'exon_intervals1': json.loads(comparison.exon_intervals1),
                'exon_intervals2': json.loads(comparison.exon_intervals2),
                'yass_output': comparison.yass_output
            })

        sequence1, extracted_gene_id1 = fetch_sequence_from_ensembl(gene_id1)
        sequence2, extracted_gene_id2 = fetch_sequence_from_ensembl(gene_id2)
        if not sequence1 or not sequence2:
            return jsonify({'error': 'Failed to fetch sequences from Ensembl.'}), 400

        fasta_file1_path = 'temp_sequence1.fasta'
        fasta_file2_path = 'temp_sequence2.fasta'
        with open(fasta_file1_path, 'wb') as file1, open(fasta_file2_path, 'wb') as file2:
            file1.write(sequence1)
            file2.write(sequence2)

        yass_output_path = 'yass_output.yop'
        yass_executable = './yass-Win64.exe'
        command = [yass_executable, fasta_file1_path, fasta_file2_path, '-o', yass_output_path]
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        yass_output = result.stdout + result.stderr

        result_sequences, directions, min_x, max_x, min_y, max_y, _, _ = process_sequences(yass_output_path)

        gene_structure1 = fetch_gene_structure(gene_id1)
        gene_structure2 = fetch_gene_structure(gene_id2)
        exon_intervals1 = {parent: [(exon['start'], exon['end']) for exon in gene_structure1 if exon['Parent'] == parent] for parent in set(exon['Parent'] for exon in gene_structure1)}
        exon_intervals2 = {parent: [(exon['start'], exon['end']) for exon in gene_structure2 if exon['Parent'] == parent] for parent in set(exon['Parent'] for exon in gene_structure2)}

        def normalize_exons(exon_intervals, min_val, max_val):
            normalized_intervals = {}
            for parent, intervals in exon_intervals.items():
                min_start = min(start for start, end in intervals)
                max_end = max(end for start, end in intervals)
                gene_length = max_end - min_start
                normalized_intervals[parent] = [(min_val + ((start - min_start) / gene_length) * (max_val - min_val), min_val + ((end - min_start) / gene_length) * (max_val - min_val)) for start, end in intervals]
            return normalized_intervals

        normalized_exons1 = normalize_exons(exon_intervals1, min_x, max_x)
        normalized_exons2 = normalize_exons(exon_intervals2, min_y, max_y)

        gene_structure1_html = create_gene_plot(normalized_exons1[list(normalized_exons1.keys())[0]], x_range=[min_x, max_x]).to_html()
        gene_structure2_html = create_gene_plot(normalized_exons2[list(normalized_exons2.keys())[0]], x_range=[min_y, max_y]).to_html()

        soup1 = BeautifulSoup(gene_structure1_html, 'html.parser')
        gene_structure1_body = soup1.body.decode_contents()
        soup2 = BeautifulSoup(gene_structure2_html, 'html.parser')
        gene_structure2_body = soup2.body.decode_contents()

        os.remove(fasta_file1_path)
        os.remove(fasta_file2_path)
        os.remove(yass_output_path)

        dotplot_data = {
            'directions': directions,
            'min_x': min_x,
            'max_x': max_x,
            'min_y': min_y,
            'max_y': max_y,
            'x_label': extracted_gene_id1,
            'y_label': extracted_gene_id2
        }

        # Save the new comparison to the database
        new_comparison = GeneComparison(
            gene_id1=gene_id1,
            gene_id2=gene_id2,
            dotplot_data=json.dumps(dotplot_data),
            gene_structure1_html=gene_structure1_body,
            gene_structure2_html=gene_structure2_body,
            exon_intervals1=json.dumps(normalized_exons1),
            exon_intervals2=json.dumps(normalized_exons2),
            yass_output=yass_output
        )
        db.session.add(new_comparison)
        db.session.commit()

        return jsonify({
            'dotplot_data': dotplot_data,
            'gene_structure1_html': gene_structure1_body,
            'gene_structure2_html': gene_structure2_body,
            'exon_intervals1': normalized_exons1,
            'exon_intervals2': normalized_exons2,
            'yass_output': yass_output
        })
    
    
# Define the update and plot endpoints
@main.route('/dash/update', methods=['POST'])#This route handles POST requests to update exon positions data
def update_exon_positions():
    data = request.json
    exons_positions = data.get('exonsPositions', [])
    return jsonify(success=True)


@main.route('/dash/dotplot/update', methods=['POST'])
def update_dotplot_data():#This route handles POST requests to update dot plot data.
    data = request.json
    dotplot_data = data.get('dotplot_data', {})# Retrieves the dot plot data from the JSON data.
    return jsonify(success=True)


@main.route('/dash/plot', methods=['GET'])#This route handles GET requests to generate and return the HTML representation of a gene structure plot based on provided exon positions.
def plot_gene_structure():
    positions = request.args.get('positions')#Retrieves the positions parameter from the query string.
    exons_positions = json.loads(positions) if positions else []#Parses the positions parameter from JSON format to a Python list.
    fig = create_gene_plot(exons_positions)#Calls create_gene_plot to generate the Plotly figure using the provided exon position
    return fig.to_html()


@main.route('/dash/dotplot/plot', methods=['POST'])
def plot_dotplot_route():
    dotplot_data = request.json['dotplot_data']
    fig = plot_dotplot(dotplot_data['directions'],
                       dotplot_data['min_x'], dotplot_data['max_x'],
                       dotplot_data['min_y'], dotplot_data['max_y'],
                       dotplot_data['x_label'], dotplot_data['y_label'])
    return fig.to_html()

if __name__ == '__main__':
    app.run(debug=True)
