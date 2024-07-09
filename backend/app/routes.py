from flask import Blueprint, request, jsonify, Flask
# from .models import GeneComparison
# from .extensions import db
import requests
import subprocess
import os
import json
from .dash_app import create_dash_app
from yop_reader import process_sequences
from bs4 import BeautifulSoup
from flask_cors import CORS
import logging
import time
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from flask_compress import Compress




app = Flask(__name__)
Compress(app)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
logging.basicConfig(level=logging.INFO)


CORS(app, supports_credentials=True, allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "OPTIONS"])

dash_app, create_gene_plot, plot_dotplot = create_dash_app(app)

main = Blueprint('main', __name__)
generate = Blueprint('generate', __name__)

def fetch_sequence_from_ensembl_parallel(gene_id):
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
    



def chunk_data(data, chunk_size=1000):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

@main.route('/run-evo-genes', methods=['POST'])
def run_evo_genes():
    start_time = time.time()
    logging.info("run_evo_genes started")

    if 'GeneID1' not in request.form or 'GeneID2' not in request.form:
        return jsonify({'error': 'GeneID1 and GeneID2 are required.'}), 400

    gene_id1 = request.form['GeneID1']
    gene_id2 = request.form['GeneID2']

    # Ensure the gene IDs are always ordered for consistency
    gene_id1, gene_id2 = sorted([gene_id1, gene_id2])

    logging.info("Fetching sequences in parallel")
    # Fetch sequences in parallel
    with ThreadPoolExecutor() as executor:
        future_seq1 = executor.submit(fetch_sequence_from_ensembl_parallel, gene_id1)
        future_seq2 = executor.submit(fetch_sequence_from_ensembl_parallel, gene_id2)
        sequence1, extracted_gene_id1 = future_seq1.result()
        sequence2, extracted_gene_id2 = future_seq2.result()

    if not sequence1 or not sequence2:
        logging.error("Failed to fetch sequences from Ensembl")
        return jsonify({'error': 'Failed to fetch sequences from Ensembl.'}), 400

    logging.info("Sequences fetched")

    # Process sequences and run YASS
    fasta_file1_path = 'temp_sequence1.fasta'
    fasta_file2_path = 'temp_sequence2.fasta'
    with open(fasta_file1_path, 'wb') as file1, open(fasta_file2_path, 'wb') as file2:
        file1.write(sequence1)
        file2.write(sequence2)

    logging.info("Running YASS")
    yass_output_path = 'yass_output.yop'
    yass_executable = './yass-Win64.exe'
    command = [yass_executable, fasta_file1_path, fasta_file2_path, '-o', yass_output_path]
    yass_start_time = time.time()
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    yass_end_time = time.time()
    logging.info(f"YASS completed in {yass_end_time - yass_start_time:.2f} seconds")
    yass_output = result.stdout + result.stderr

    result_sequences, directions, min_x, max_x, min_y, max_y, _, _ ,inverted = process_sequences(yass_output_path)
    if result_sequences is None:
        return jsonify({'message': 'No alignment found.'}), 200


    logging.info("Sequences processed")

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

    gene_structure1_plot = create_gene_plot(normalized_exons1[list(normalized_exons1.keys())[0]], x_range=[min_x, max_x])
    gene_structure2_plot = create_gene_plot(normalized_exons2[list(normalized_exons2.keys())[0]], x_range=[min_y, max_y])

    # os.remove(fasta_file1_path)
    # os.remove(fasta_file2_path)
    # os.remove(yass_output_path)

    dotplot_data = {
        'directions': directions,
        'min_x': min_x,
        'max_x': max_x,
        'min_y': min_y,
        'max_y': max_y,
        'x_label': extracted_gene_id1,
        'y_label': extracted_gene_id2,
        'sampling_fraction': request.form.get('samplingFraction', '0.1'), # Get the sampling fraction from the request
        'inverted': inverted

    }

    dotplot_plot = plot_dotplot(**dotplot_data)

    end_time = time.time()
    logging.info(f"run_evo_genes completed in {end_time - start_time:.2f} seconds")

    return_data = {
        'dotplot_plot': dotplot_plot.to_dict(),
        'gene_structure1_plot': gene_structure1_plot.to_dict(),
        'gene_structure2_plot': gene_structure2_plot.to_dict(),
        'exon_intervals1': normalized_exons1,
        'exon_intervals2': normalized_exons2,
        'yass_output': yass_output,
        'data_for_manual_zoom': dotplot_data
    }

    # print(json.dumps(return_data, indent=4)) 
    return jsonify(return_data)
    
@main.route('/dash/update', methods=['POST'])
def update_exon_positions():
    data = request.json
    exons_positions = data.get('exonsPositions', [])
    # Process and return data if needed
    return jsonify(success=True)


@main.route('/dash/dotplot/update', methods=['POST'])
def update_dotplot_data():#This route handles POST requests to update dot plot data.
    data = request.json
    dotplot_data = data.get('dotplot_data', {})# Retrieves the dot plot data from the JSON data.
    return jsonify(success=True)


@main.route('/dash/dotplot/plot', methods=['POST'])
def plot_dotplot_route():
    dotplot_data = request.json['dotplot_data']
    fig = plot_dotplot(
        dotplot_data['directions'],
        dotplot_data['min_x'], dotplot_data['max_x'],
        dotplot_data['min_y'], dotplot_data['max_y'],
        dotplot_data['x_label'], dotplot_data['y_label'],
        sampling_fraction=dotplot_data.get('sampling_fraction', '0.1'),
        inverted=dotplot_data.get('inverted', False)
    )
    return jsonify(fig.to_dict())

# @main.route('/dash/plot', methods=['POST'])
# def plot_gene_structure():
#     data = request.json
#     exons_positions = data.get('exonsPositions', [])
#     fig = create_gene_plot(exons_positions)
#     return jsonify(fig.to_dict())

@main.route('/dash/plot', methods=['POST'])
def plot_gene_structure():
    data = request.json
    exons_positions = data.get('exonsPositions', [])
    is_vertical = data.get('isVertical', False)  # Get the isVertical parameter from the request
    fig = create_gene_plot(exons_positions, is_vertical=is_vertical)  # Pass is_vertical to create_gene_plot
    return jsonify(fig.to_dict())



@main.route('/dash/dotplot/plot_update', methods=['POST'])
def plot_dotplot_route_update():

    start_time = time.time()
    logging.info("manual zoom started")

    data = request.json
    # print(f"Received data: {data}")  # Log received data

    if 'dotplot_data' not in data:
        print("Error: dotplot_data is missing from the request")
        return jsonify({'error': 'dotplot_data is missing from the request'}), 400

    dotplot_data = data['dotplot_data']

    if 'min_x' not in dotplot_data:
        print("Error: min_x is missing from dotplot_data")
        return jsonify({'error': 'min_x is missing from dotplot_data'}), 400

    # Extract the original min and max values
    original_min_x = dotplot_data['min_x']
    original_max_x = dotplot_data['max_x']
    original_min_y = dotplot_data['min_y']
    original_max_y = dotplot_data['max_y']

    # print(dotplot_data['directions'])
    print(len(dotplot_data['directions']))
    # Extract the zoom coordinates from the request
    x1 = data.get('x1')
    x2 = data.get('x2')
    y1 = data.get('y1')
    y2 = data.get('y2')
    sampling_fraction = data.get('sampling_fraction', '0.1')  # Get the sampling fraction from the request

    # Validate that x1, x2, y1, y2 are not None
    if x1 is None or x2 is None or y1 is None or y2 is None:
        print("Error: Zoom coordinates are required")
        return jsonify({'error': 'Zoom coordinates are required'}), 400

    # Ensure x1 < x2 and y1 < y2
    if x1 >= x2 or y1 >= y2:
        print("Error: Invalid zoom coordinates: x1 should be less than x2 and y1 should be less than y2")
        return jsonify({'error': 'Invalid zoom coordinates: x1 should be less than x2 and y1 should be less than y2'}), 400

    # Validate that x1, x2, y1, y2 are not Zero
    if x1 == 0:
        x1 += 1
    if x2 == 0:
        x2 = 1
    if y1 == 0:
        y1 = 1
    if y2 == 0:
        y2 = 1

    # Validate the coordinates are within the original min/max range
    if not (original_min_x <= x1 <= original_max_x and
            original_min_x <= x2 <= original_max_x and
            original_min_y <= y1 <= original_max_y and
            original_min_y <= y2 <= original_max_y):
        print("Error: Zoom coordinates are out of range")
        return jsonify({'error': 'Zoom coordinates are out of range'}), 400

    # Update the dotplot data with the new coordinates
    dotplot_data['min_x'] = x1
    dotplot_data['max_x'] = x2
    dotplot_data['min_y'] = y1
    dotplot_data['max_y'] = y2

    filtered_directions = []
    for direction in dotplot_data['directions']:
        points = np.array(direction[0])  # Convert list of points to numpy array
        mask = (points[:, 0] >= x1) & (points[:, 0] <= x2) & (points[:, 1] >= y1) & (points[:, 1] <= y2)
        if np.any(mask):
            filtered_directions.append(direction)

    dotplot_data['directions'] = filtered_directions

    print("new directions lenght:   ", len(dotplot_data['directions']))

    # Generate the updated plot
    fig = plot_dotplot(
        dotplot_data['directions'],
        dotplot_data['min_x'],
        dotplot_data['max_x'],
        dotplot_data['min_y'],
        dotplot_data['max_y'],
        dotplot_data['x_label'],
        dotplot_data['y_label'],
        sampling_fraction=sampling_fraction,  # Pass the sampling fraction
        inverted=dotplot_data.get('inverted', False)

    )

    # Update gene structure plots based on the new zoom levels
    exon_intervals1 = data.get('exon_intervals1', {})
    exon_intervals2 = data.get('exon_intervals2', {})
    x_label = dotplot_data['x_label']
    y_label = dotplot_data['y_label']

    # Ensure consistent ranges for all plots
    x_range = [x1, x2]
    y_range = [y1, y2]

    # Update gene structure plots based on the new zoom levels
    gene_structure1_plot = create_gene_plot(exon_intervals1[list(exon_intervals1.keys())[0]], x_range=x_range)
    gene_structure2_plot = create_gene_plot(exon_intervals2[list(exon_intervals2.keys())[0]], x_range=y_range)

    end_time = time.time()
    logging.info(f"manual zoom completed in {end_time - start_time:.2f} seconds")

    return jsonify({
        'gene_structure1_plot': gene_structure1_plot.to_dict(),
        'gene_structure2_plot': gene_structure2_plot.to_dict(),
        'dotplot_plot': fig.to_dict()
    })
@main.route('/dash/relayout', methods=['POST'])
def handle_relayout():
    try:
        relayout_data = request.json
        # print(f"Received relayout data: {relayout_data}")

        x0 = relayout_data.get('x0')
        x1 = relayout_data.get('x1')
        y0 = relayout_data.get('y0')
        y1 = relayout_data.get('y1')
        exon_intervals1 = relayout_data.get('exon_intervals1', {})
        exon_intervals2 = relayout_data.get('exon_intervals2', {})
        x_label = relayout_data['dotplot_data']['layout']['x_label']
        y_label = relayout_data['dotplot_data']['layout']['y_label']

        print(f"Zoom coordinates: x0={x0}, x1={x1}, y0={y0}, y1={y1}")

        # Ensure consistent ranges for all plots
        x_range = [x0, x1]
        y_range = [y0, y1]  # Adjust y range as needed to match Plotly's coordinate system

        # Update gene structure plots based on the new zoom levels
        gene_structure1_plot = create_gene_plot(exon_intervals1[list(exon_intervals1.keys())[0]], x_range=x_range, is_vertical=False)
        gene_structure2_plot = create_gene_plot(exon_intervals2[list(exon_intervals2.keys())[0]], x_range=y_range, is_vertical=True)

        # Update the dotplot layout based on the new zoom levels
        dotplot_data = relayout_data.get('dotplot_data', {})
        dotplot_layout = dotplot_data.get('layout', {})

        dotplot_layout['xaxis'] = {
            'range': x_range,
            'showgrid': False,
            'title': {'text': x_label},
            'type': 'linear',
            'autorange': False
        }
        dotplot_layout['yaxis'] = {
            'range': y_range,
            'showgrid': False,
            'showticklabels': True,
            'side': 'right',
            'title': {'text': y_label},
            'type': 'linear',
            'autorange': False
        }

        dotplot_plot = {
            'data': dotplot_data.get('data', []),
            'layout': dotplot_layout
        }

        return jsonify({
            'gene_structure1_plot': gene_structure1_plot.to_dict(),
            'gene_structure2_plot': gene_structure2_plot.to_dict(),
            'dotplot_plot': dotplot_plot
        })
    except Exception as e:
        print(f'Error processing relayout data: {e}')
        return jsonify(success=False, error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
    from werkzeug.middleware.proxy_fix import ProxyFix
    from gevent.pywsgi import WSGIServer

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
