from flask import Blueprint, request, jsonify, Flask
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



# Initialize Flask application

app = Flask(__name__)
Compress(app)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024 # Set maximum upload size to 500 MB
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0# Disable caching for static files
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Set session lifetime to 1 hour
logging.basicConfig(level=logging.INFO)# Set logging level to INFO

# Enable Cross-Origin Resource Sharing (CORS)

CORS(app, supports_credentials=True, allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "OPTIONS"])
# Initialize Dash app and get references to necessary plotting functions
dash_app, create_gene_plot, plot_dotplot = create_dash_app(app)


# Define blueprints for organizing routes
main = Blueprint('main', __name__)
generate = Blueprint('generate', __name__)

# Function to fetch gene information using Ensembl API
def fetch_gene_info(gene_id):
    # Define the URL for the Ensembl API to fetch gene information using the provided gene ID.
    url = f"https://rest.ensembl.org/lookup/id/{gene_id}"
    # Set the headers to indicate that the response should be in JSON format.
    headers = {"Content-Type": "application/json"}
    # Make a GET request to the Ensembl API to fetch the gene information.
    response = requests.get(url, headers=headers)
    
    # Check if the response status code is not 200 (OK).
    # If the request was unsuccessful, return None for both gene_name and species_name.
    if response.status_code != 200:
        return None, None
    
    # Parse the JSON response content into a Python dictionary.
    data = response.json()
    # If the 'display_name' key is not found, default to "Unknown".
    gene_name = data.get("display_name", "Unknown")
    # Extract the species name from the response data.
    # The species name is formatted with underscores, so they are replaced with spaces.
    # The 'title()' method is used to capitalize the first letter of each word.
    species_name = data.get("species", "Unknown").replace('_', ' ').title()
    
    # Return the extracted gene name and species name.
    return gene_name, species_name


# Function to fetch gene sequence from Ensembl API in parallel
def fetch_sequence_from_ensembl_parallel(gene_id):
    # Construct the URL for the Ensembl REST API to fetch the gene sequence in FASTA format.
    ensembl_url = f'https://rest.ensembl.org/sequence/id/{gene_id}?content-type=text/x-fasta'
    # Make a GET request to the Ensembl API to fetch the gene sequence.
    response = requests.get(ensembl_url)
    if response.ok:
        # Decode the sequence data from bytes to a UTF-8 string.
        sequence = response.content.decode('utf-8')
         # Extract the gene ID from the first line of the FASTA format.
        # The FASTA format starts with a line beginning with '>', followed by the gene ID and description.       
        gene_id_extracted = sequence.split('\n', 1)[0].split()[0].lstrip('>')
        # Return the sequence as bytes (encoded in UTF-8) and the extracted gene ID.
        return sequence.encode('utf-8'), gene_id_extracted
    else:
        return None, None

# Function to fetch gene structure (transcripts and exons) from Ensembl API
def fetch_gene_structure(gene_ensembl_id, content_type='application/json'):
    server = "https://rest.ensembl.org"
    
    # Step 1: Fetch and filter transcripts
    transcript_endpoint = f"/overlap/id/{gene_ensembl_id}?feature=transcript"
    try:
        # Send a GET request to fetch the transcripts associated with the gene ID
        r_transcript = requests.get(server + transcript_endpoint, headers={"Accept": content_type})
        r_transcript.raise_for_status()# Raise an HTTPError if the request returned an unsuccessful status code
        transcripts = r_transcript.json()# Parse the JSON response to get a list of transcripts
        
        # Filter transcripts and store their strand information
        # Only keep transcripts that belong to the given gene ID
        filtered_transcripts = {
            transcript['transcript_id']: transcript['strand']
            for transcript in transcripts 
            if transcript['Parent'] == gene_ensembl_id
        }
        
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching transcripts for gene_id {gene_ensembl_id}: {e}")
        return []

    # Step 2: Fetch and filter exons
    exon_endpoint = f"/overlap/id/{gene_ensembl_id}?feature=exon"
    try:
        # Send a GET request to fetch the exons associated with the gene ID        
        r_exon = requests.get(server + exon_endpoint, headers={"Accept": content_type})
        r_exon.raise_for_status()
        all_exons = r_exon.json()# Parse the JSON response to get a list of exons
        
        # Filter exons based on their parent transcript IDs
        # Only keep exons that belong to transcripts in the filtered_transcripts dictionary
        filtered_exons = [
            {'start': exon['start'], 'end': exon['end'], 'Parent': exon['Parent']}
            for exon in all_exons
            if exon['Parent'] in filtered_transcripts
        ]
        # Return the filtered exons and the filtered transcripts with their strand information        
        return filtered_exons, filtered_transcripts
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exons for gene_id {gene_ensembl_id}: {e}")
        return [], {}
    
# Function to reverse the order of exons on the negative strand
def reverse_negative_strand_exons(exon_intervals):
    if not exon_intervals:
        return []

    # Sort the exon intervals by their start position to ensure they are in the correct order
    sorted_intervals = sorted(exon_intervals, key=lambda x: x[0])

    # Calculate total gene length
    # Determine the start and end of the entire gene based on the sorted exons
    gene_start = sorted_intervals[0][0]
    gene_end = sorted_intervals[-1][1]
    gene_length = gene_end - gene_start

    # Calculate the sizes of each exon (difference between start and end positions)
    exon_sizes = [end - start for start, end in sorted_intervals]
    # Calculate the distances between consecutive exons (inter-exon distances)
    inter_exon_distances = [sorted_intervals[i+1][0] - sorted_intervals[i][1] for i in range(len(sorted_intervals) - 1)]

    # Reverse the order of exon sizes and inter-exon distances to reflect the negative strand
    reversed_sizes = exon_sizes[::-1]
    reversed_distances = inter_exon_distances[::-1]

    # Reconstruct the reversed exons by iterating through the reversed sizes and distances
    reversed_exons = []
    current_start = gene_start
    for i, size in enumerate(reversed_sizes):
        exon_end = current_start + size# Calculate the end position of the current exon
        reversed_exons.append((current_start, exon_end))# Add the reversed exon to the list
        if i < len(reversed_distances):# If there are more distances, update the start position for the next exon
            current_start = exon_end + reversed_distances[i]
    # Return the list of reversed exons
    return reversed_exons


# Function to normalize exon positions based on a minimum value
def normalize_exons(exon_intervals, min_val):
    normalized_intervals = {}
    # Iterate over each parent transcript and its associated strand value and exon intervals
    for parent, (strand_value, intervals) in exon_intervals.items():
        # Find the minimum start position and maximum end position of the exons for this parent
        min_start = min(start for start, end in intervals)
        max_end = max(end for start, end in intervals)
        # Normalize the exon intervals by shifting them to start at the provided min_val
        normalized = [(min_val + (start - min_start), end - min_start + min_val) for start, end in intervals]
         # If the strand is negative (strand_value == -1), reverse the normalized exons       
        if strand_value == -1:
            normalized = reverse_negative_strand_exons(normalized)
        # Store the normalized (and possibly reversed) intervals in the dictionary, keyed by the parent transcript ID
        normalized_intervals[parent] = normalized
    return normalized_intervals

# Route to run the evolutionary gene analysis
@main.route('/run-evo-genes', methods=['POST'])
def run_evo_genes():
    start_time = time.time()
    logging.info("run_evo_genes started")

    # Check if the required form data (GeneID1 and GeneID2) is present in the request
    if 'GeneID1' not in request.form or 'GeneID2' not in request.form:
        return jsonify({'error': 'GeneID1 and GeneID2 are required.'}), 400
   
    # Retrieve and clean the gene IDs from the form data
    raw_gene_id1 = request.form['GeneID1']
    raw_gene_id2 = request.form['GeneID2']


    # Strip whitespace, newlines, and spaces from the gene IDs to ensure they are properly formatted
    gene_id1 = raw_gene_id1.strip().replace("\n", "").replace("\r", "").replace(" ", "")
    gene_id2 = raw_gene_id2.strip().replace("\n", "").replace("\r", "").replace(" ", "")

    # Fetch gene names and species names for each gene ID using the Ensembl API
    gene_name1, species_name1 = fetch_gene_info(gene_id1)
    gene_name2, species_name2 = fetch_gene_info(gene_id2)

    logging.info("Fetching sequences in parallel")
    # Use ThreadPoolExecutor to fetch gene sequences in parallel to improve performance
    with ThreadPoolExecutor() as executor:
        future_seq1 = executor.submit(fetch_sequence_from_ensembl_parallel, gene_id1)
        future_seq2 = executor.submit(fetch_sequence_from_ensembl_parallel, gene_id2)
        sequence1, extracted_gene_id1 = future_seq1.result()
        sequence2, extracted_gene_id2 = future_seq2.result()


    # If either sequence could not be fetched, log an error and return a 400 response
    if not sequence1 or not sequence2:
        logging.error("Failed to fetch sequences from Ensembl")
        return jsonify({'error': 'Failed to fetch sequences from Ensembl.'}), 400

    logging.info("Sequences fetched")

    # Ensure the longer gene sequence is always used for the X-axis by swapping if necessary
    if len(sequence2) > len(sequence1):
        gene_id1, gene_id2 = gene_id2, gene_id1
        sequence1, sequence2 = sequence2, sequence1
        extracted_gene_id1, extracted_gene_id2 = extracted_gene_id2, extracted_gene_id1
        gene_name1, gene_name2 = gene_name2, gene_name1
        species_name1, species_name2 = species_name2, species_name1


    # Write the fetched sequences to temporary FASTA files for processing with YASS
    fasta_file1_path = 'temp_sequence1.fasta'
    fasta_file2_path = 'temp_sequence2.fasta'
    with open(fasta_file1_path, 'wb') as file1, open(fasta_file2_path, 'wb') as file2:
        file1.write(sequence1)
        file2.write(sequence2)

    # logging.info(f"Sequences: sequence1={sequence1[:50]}..., sequence2={sequence2[:50]}...")  # Print part of the sequences for verification
    logging.info("Running YASS")
    # Define the YASS executable and the command line arguments for running YASS
    yass_output_path = 'yass_output.yop'
    yass_executable = './yass-Win64.exe'
    command = [
    yass_executable, 
    fasta_file1_path, 
    fasta_file2_path, 
    '-o', yass_output_path, 
    '-O', '1000000', 
    '-C', '5,-4,-3,-4', 
    '-E', '10', 
    '-G', '-16,-4', 
    '-W', '20,40000', 
    '-X', '30', 
    '-c', '1', 
    '-d', '1', 
    '-e', '2.8', 
    '-i', '10', 
    '-m', '25', 
    '-p', '#@#--#---#-@##,###-#@-#-@#', 
    '-r', '2', 
    '-s', '70', 
    '-w', '4'
    ]
    # Run the YASS tool to perform sequence alignment, and measure the time taken
    yass_start_time = time.time()
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    yass_end_time = time.time()
    logging.info(f"YASS completed in {yass_end_time - yass_start_time:.2f} seconds")
    yass_output = result.stdout + result.stderr

    # Process the output from YASS to extract relevant sequence information and alignment details
    result_sequences, directions, min_x, max_x, min_y, max_y, _, _ ,inverted = process_sequences(yass_output_path)
    # If no alignment was found, return a message indicating this
    if result_sequences is None:
        return jsonify({'message': 'No alignment found.'}), 200


    logging.info("Sequences processed")
    # Fetch the gene structure (exons and transcripts) for both gene IDs
    gene_structure1, transcripts1 = fetch_gene_structure(gene_id1)
    gene_structure2, transcripts2 = fetch_gene_structure(gene_id2)
    
    # Extract and normalize the exon intervals for both gene structures
    exon_intervals1 = {parent: [(exon['start'], exon['end']) for exon in gene_structure1 if exon['Parent'] == parent] for parent in set(exon['Parent'] for exon in gene_structure1)}
    exon_intervals2 = {parent: [(exon['start'], exon['end']) for exon in gene_structure2 if exon['Parent'] == parent] for parent in set(exon['Parent'] for exon in gene_structure2)}
    
    # Normalize the exons based on the minimum X and Y values from the alignment
    normalized_exons1 = normalize_exons(
        {parent: (transcripts1[parent], intervals) for parent, intervals in exon_intervals1.items()},
        min_x
    )
    normalized_exons2 = normalize_exons(
        {parent: (transcripts2[parent], intervals) for parent, intervals in exon_intervals2.items()},
        min_y
    )
    # Create plots for the gene structures using the normalized exon intervals
    gene_structure1_plot = create_gene_plot(normalized_exons1[list(normalized_exons1.keys())[0]], x_range=[min_x, max_x])
    gene_structure2_plot = create_gene_plot(normalized_exons2[list(normalized_exons2.keys())[0]], x_range=[min_y, max_y])
    
    # Clean up temporary files created for YASS processing
    os.remove(fasta_file1_path)
    os.remove(fasta_file2_path)
    os.remove(yass_output_path)

    # Prepare the data for the dot plot and gene structure plots
    dotplot_data = {
        'directions': directions,
        'min_x': min_x,
        'max_x': max_x,
        'min_y': min_y,
        'max_y': max_y,
        'x_label': f"{gene_name1} ({species_name1}) - {extracted_gene_id1}",
        'y_label': f"{gene_name2} ({species_name2}) - {extracted_gene_id2}",
        'sampling_fraction': request.form.get('samplingFraction', '0.1'), # Get the sampling fraction from the request
        'inverted': inverted

    }
    # Create the dot plot using the prepared data
    dotplot_plot = plot_dotplot(**dotplot_data)

    end_time = time.time()
    logging.info(f"run_evo_genes completed in {end_time - start_time:.2f} seconds")
    # Prepare the response data, including the dot plot, gene structure plots, and YASS output
    return_data = {
        'dotplot_plot': dotplot_plot.to_dict(),
        'gene_structure1_plot': gene_structure1_plot.to_dict(),
        'gene_structure2_plot': gene_structure2_plot.to_dict(),
        'exon_intervals1': normalized_exons1,
        'exon_intervals2': normalized_exons2,
        'yass_output': yass_output,
        'data_for_manual_zoom': dotplot_data
    }

    return jsonify(return_data)
    
@main.route('/dash/update', methods=['POST'])
def update_exon_positions():
    # Retrieve JSON data from the request body
    data = request.json
    # Extract the 'exonsPositions' field from the JSON data. 
    # If it's not found, default to an empty list.
    exons_positions = data.get('exonsPositions', [])
    # Process and return data if needed
    return jsonify(success=True)


@main.route('/dash/dotplot/update', methods=['POST'])
def update_dotplot_data():#This route handles POST requests to update dot plot data.
    # Retrieve JSON data from the request body
    data = request.json
    
    # Extract the 'dotplot_data' field from the JSON data. 
    # If it's not found, default to an empty dictionary.
    dotplot_data = data.get('dotplot_data', {})# Retrieves the dot plot data from the JSON data.
    return jsonify(success=True)


@main.route('/dash/dotplot/plot', methods=['POST'])
def plot_dotplot_route():
    # Retrieve the 'dotplot_data' field from the JSON data in the request body
    dotplot_data = request.json['dotplot_data']
    # Generate a dot plot using the data provided in the request
    fig = plot_dotplot(
        dotplot_data['directions'],
        dotplot_data['min_x'], dotplot_data['max_x'],
        dotplot_data['min_y'], dotplot_data['max_y'],
        dotplot_data['x_label'], dotplot_data['y_label'],
        sampling_fraction=dotplot_data.get('sampling_fraction', '0.1'),
        inverted=dotplot_data.get('inverted', False)
    )
    return jsonify(fig.to_dict())



@main.route('/dash/plot', methods=['POST'])
def plot_gene_structure():
    data = request.json
    # Extract the 'exonsPositions' field from the JSON data. 
    # If it's not found, default to an empty list.
    exons_positions = data.get('exonsPositions', [])
    # Extract the 'isVertical' field from the JSON data to determine plot orientation.
    # Default to False (horizontal) if not provided.
    is_vertical = data.get('isVertical', False)  # Get the isVertical parameter from the request
    # print(f"Received isVertical: {is_vertical}") 
    fig = create_gene_plot(exons_positions, is_vertical=is_vertical)  # Pass is_vertical to create_gene_plot
    return jsonify(fig.to_dict())


#this function responsible for the manual zoom 
@main.route('/dash/dotplot/plot_update', methods=['POST'])
def plot_dotplot_route_update():

    start_time = time.time()
    logging.info("manual zoom started")

    data = request.json
    # print(f"Received data: {data}")  # Log received data
    # Check if 'dotplot_data' is present in the request data
    if 'dotplot_data' not in data:
        error_message = "Error: dotplot_data is missing from the request"
        print(error_message)
        return jsonify({'error': error_message}), 400

    dotplot_data = data['dotplot_data']
    # Validate that the minimum x-coordinate (min_x) is present in the dotplot_data
    if 'min_x' not in dotplot_data:
        error_message = "Error: min_x is missing from dotplot_data"
        print(error_message)
        return jsonify({'error': error_message}), 400

    # Extract the original min and max values for the x and y coordinates
    original_min_x = dotplot_data['min_x']
    original_max_x = dotplot_data['max_x']
    original_min_y = dotplot_data['min_y']
    original_max_y = dotplot_data['max_y']

    # Extract the zoom coordinates from the request data
    x1 = data.get('x1')
    x2 = data.get('x2')
    y1 = data.get('y1')
    y2 = data.get('y2')
    sampling_fraction = data.get('sampling_fraction', '0.1')  # Get the sampling fraction from the request

    # Validate that the zoom coordinates (x1, x2, y1, y2) are present
    if x1 is None or x2 is None or y1 is None or y2 is None:
        error_message = "Error: Zoom coordinates are required"
        print(error_message)
        return jsonify({'error': error_message}), 400

    # Ensure that x1 < x2 and y1 < y2
    if x1 >= x2 or y1 >= y2:
        error_message = "Error: Invalid zoom coordinates: x1 should be less than x2 and y1 should be less than y2"
        print(error_message)
        return jsonify({'error': error_message}), 400

    # Validate that x1, x2, y1, y2 are not Zero
    if x1 == 0:
        x1 += 1
    if x2 == 0:
        x2 = 1
    if y1 == 0:
        y1 = 1
    if y2 == 0:
        y2 = 1

    # Ensure that the coordinates are within the original min/max range
    if not (original_min_x <= x1 <= original_max_x and
            original_min_x <= x2 <= original_max_x and
            original_min_y <= y1 <= original_max_y and
            original_min_y <= y2 <= original_max_y):
        error_message = "Error: Zoom coordinates are out of range"
        return jsonify({'error': error_message}), 400

    # Update the dotplot data with the new zoom coordinates
    dotplot_data['min_x'] = x1
    dotplot_data['max_x'] = x2
    dotplot_data['min_y'] = y1
    dotplot_data['max_y'] = y2

    # Filter the directions to include only those within the new zoom range
    filtered_directions = []
    for direction in dotplot_data['directions']:
        points = np.array(direction[0])  # Convert list of points to numpy array
        mask = (points[:, 0] >= x1) & (points[:, 0] <= x2) & (points[:, 1] >= y1) & (points[:, 1] <= y2)
        if np.any(mask):
            filtered_directions.append(direction)

    dotplot_data['directions'] = filtered_directions


    # Generate the updated dot plot with the new zoom coordinates
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

    # Create the gene structure plots with the new zoom levels
    gene_structure1_plot = create_gene_plot(exon_intervals1[list(exon_intervals1.keys())[0]], x_range=x_range)
    gene_structure2_plot = create_gene_plot(exon_intervals2[list(exon_intervals2.keys())[0]], x_range=y_range)

    end_time = time.time()
    logging.info(f"manual zoom completed in {end_time - start_time:.2f} seconds")
    
    # Return the updated plots as JSON objects
    return jsonify({
        'gene_structure1_plot': gene_structure1_plot.to_dict(),
        'gene_structure2_plot': gene_structure2_plot.to_dict(),
        'dotplot_plot': fig.to_dict()
    })


#this function responsible for updaiting the dotplot limits after changing to a different transcript  
@main.route('/dash/dotplot/update_limits', methods=['POST'])
def update_dotplot_limits():
    data = request.json
    try:
        dotplot_data = data['dotplot_data']
        # Extract necessary data from the request
        x1 = data['x1']
        x2 = data['x2']
        y1 = data['y1']
        y2 = data['y2']
        sampling_fraction = data['sampling_fraction']
        exon_intervals1 = data['exon_intervals1']
        exon_intervals2 = data['exon_intervals2']
        inverted = data['inverted']

        # Update the dotplot data with new limits and parameters
        dotplot_data.update({
            'min_x': x1,
            'max_x': x2,
            'min_y': y1,
            'max_y': y2,
            'sampling_fraction': sampling_fraction,
            'inverted': inverted
        })

        # Generate a new dot plot with the updated limits
        fig = plot_dotplot(**dotplot_data)

        # Generate updated gene structure plots for both sets of exon intervals
        gene_structure1_plot = create_gene_plot(exon_intervals1, x_range=[x1, x2])
        gene_structure2_plot = create_gene_plot(exon_intervals2, x_range=[y1, y2])
       
        # Return the updated dot plot and gene structure plots as JSON objects
        return jsonify({
            'dotplot_plot': fig.to_dict(),
            'gene_structure1_plot': gene_structure1_plot.to_dict(),
            'gene_structure2_plot': gene_structure2_plot.to_dict()
        })
    except KeyError as e:
        logging.error(f"Missing key in request data: {e}")
        return jsonify({'error': f"Missing key in request data: {e}"}), 400
    except ValueError as e:
        logging.error(f"Value error in request data: {e}")
        return jsonify({'error': f"Value error in request data: {e}"}), 400
    except Exception as e:
        logging.error(f"Error processing dotplot limits: {e}")
        return jsonify({'error': f"Error processing dotplot limits: {e}"}), 500

#this function responsible for the synced zoom 
@main.route('/dash/relayout', methods=['POST'])
def handle_relayout():
    try:
        relayout_data = request.json
        # Extract the zoom coordinates from the relayout data
        x0 = relayout_data.get('x0')
        x1 = relayout_data.get('x1')
        y0 = relayout_data.get('y0')
        y1 = relayout_data.get('y1')

        # Extract exon intervals and dotplot data from the relayout data
        exon_intervals1 = relayout_data.get('exon_intervals1', {})
        exon_intervals2 = relayout_data.get('exon_intervals2', {})
        x_label = relayout_data['dotplot_data']['layout']['x_label']
        y_label = relayout_data['dotplot_data']['layout']['y_label']

        # Ensure consistent ranges for all plots
        x_range = [x0, x1]
        y_range = [y0, y1]  # Keep original order for dotplot

        # Update gene structure plots based on the new zoom levels
        gene_structure1_plot = create_gene_plot(exon_intervals1[list(exon_intervals1.keys())[0]], x_range=x_range, is_vertical=False)
        gene_structure2_plot = create_gene_plot(exon_intervals2[list(exon_intervals2.keys())[0]], x_range=[y1, y0], is_vertical=True)

        # Update the dotplot layout based on the new zoom levels
        dotplot_data = relayout_data.get('dotplot_data', {})
        dotplot_layout = dotplot_data.get('layout', {})

        # Update the X-axis configuration in the layout
        dotplot_layout['xaxis'] = {
            'range': x_range,
            'showgrid': False,
            'title': {'text': x_label},
            'type': 'linear',
            'autorange': False
        }
        # Update the Y-axis configuration in the layout
        dotplot_layout['yaxis'] = {
            'range': y_range,  # Use original y_range here
            'showgrid': False,
            'showticklabels': True,
            'side': 'right',
            'title': {'text': y_label},
            'type': 'linear',
            'autorange': False
        }

        # Combine the updated data and layout into a new dotplot
        dotplot_plot = {
            'data': dotplot_data.get('data', []),
            'layout': dotplot_layout
        }
        # Return the updated gene structure plots and dotplot as JSON objects
        return jsonify({
            'gene_structure1_plot': gene_structure1_plot.to_dict(),
            'gene_structure2_plot': gene_structure2_plot.to_dict(),
            'dotplot_plot': dotplot_plot
        })
    except Exception as e:
        print(f'Error processing relayout data: {e}')
        return jsonify(success=False, error=str(e)), 500
    

if __name__ == '__main__':
    # Run the Flask application in debug mode for development purposes
    app.run(debug=True)
    
    # Import the ProxyFix middleware from the Werkzeug library
    from werkzeug.middleware.proxy_fix import ProxyFix
    
    # Import the WSGIServer from gevent to run the application with gevent
    from gevent.pywsgi import WSGIServer

    # Apply the ProxyFix middleware to the Flask app to handle reverse proxy setups
    # ProxyFix corrects request headers when the app is behind a reverse proxy (e.g., Nginx)
    # x_for, x_proto, x_host, x_port parameters specify the number of values to trust in the respective headers
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
    
    # Create a WSGIServer instance with the gevent server
    # This runs the Flask app on all available IP addresses (0.0.0.0) on port 5000
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    
    # Start the server and keep it running to handle incoming requests
    http_server.serve_forever()
