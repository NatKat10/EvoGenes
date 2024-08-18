import re
import sys
import matplotlib.pyplot as plt
from tqdm import tqdm  # for progress bar
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import plotly.graph_objs as go




def parse_yop(file_path):
    sequences = []# Initialize an empty list to store sequences
    current_sequence = []# Initialize a list to store the current sequence being parsed

    # Pre-compiled regular expression to match the start of a sequence
    sequence_start_pattern = re.compile(r"^\*\((\d+)-(\d+)\)\((\d+)-(\d+)\) Ev: \S+ s: \d+/\d+ [fr]")

    with open(file_path, 'r', encoding='utf-8') as file:
        # Iterate through each line in the file
        for line in file:
            # Check if the line matches the sequence start pattern
            if sequence_start_pattern.match(line):
                # If a sequence is already being tracked, add it to the sequences list
                if current_sequence:
                    sequences.append(current_sequence)
                    current_sequence = []# Reset current sequence for the next one
            # Add the current line to the current sequence, stripping any leading/trailing whitespace
            current_sequence.append(line.strip())
        # After the loop, check if there's a final sequence that hasn't been added to sequences
        if current_sequence:
            sequences.append(current_sequence)
    # Return the list of sequences parsed from the file
    return sequences

def extract_fields(sequence):
    fields = {} # Initialize an empty dictionary to store extracted fields
    first_line = sequence[0]# The first line of the sequence typically contains key information
    # Regular expression to extract coordinates and direction from the first line of the sequence
    match = re.match(r"^\*\((\d+)-(\d+)\)\((\d+)-(\d+)\) Ev: \S+ s: \d+/\d+ ([fr])", first_line)
    if not match:
        return None
    # Extract the start and end positions and the direction from the match groups
    start1, end1, start2, end2, direction = match.groups()
    # Store the extracted coordinates as integers and direction in the fields dictionary
    fields['indexes'] = (int(start1), int(end1), int(start2), int(end2))
    fields['direction'] = direction

    # The second line typically contains labels for the X and Y axes
    second_line = sequence[1]
    labels_match = re.match(r'^\* "([^"]+)" \(\d+ bp\) / "([^"]+)" \(\d+ bp\)', second_line)
    # If the labels are found, extract them; otherwise, use default labels
    if labels_match:
        fields['x_label'], fields['y_label'] = labels_match.groups()
    else:
        fields['x_label'], fields['y_label'] = 'X-axis', 'Y-axis'
    # Concatenate all lines that consist only of '|' , ':' , '.' , or spaces (mutation line)
    mutation_line = ''.join(line.strip() for line in sequence if re.fullmatch(r'[|:. ]+', line.strip()))

    if mutation_line is None:
        return None
    # Store the mutation line in the fields dictionary
    fields['mutation_line'] = mutation_line


    return fields

def generate_list(fields):
    # Unpack the start and end positions for both sequences from the fields dictionary
    start1, end1, start2, end2 = fields['indexes']
    mutation_line = fields['mutation_line']
    # Determine the starting indices and steps based on the direction of the sequence
    result_list = []
    if fields['direction'] == 'f':# Forward direction
        index1, index2 = start1, start2
        step1, step2 = 1, 1# Both x and y coordinates increment
    else:# Reverse direction
        index1, index2 = start1, start2
        step1, step2 = -1, 1  # x decrements, y increments
    # Iterate over each character in the mutation line
    for char in mutation_line:
        if char == ' ':# If the character is a space, just move to the next position
            index1 += step1
            index2 += step2
            continue
        # Each character represents a type of alignment/mutation:
        elif char == '|':
            result_list.append((index1, index2, 3))  # 3 indicates the highest intensity match
            
        elif char == ':':
            result_list.append((index1, index2, 2))# 2 indicates a moderate intensity match

        elif char == '.':
            result_list.append((index1, index2, 1))# 1 indicates the lowest intensity match
        # After processing each character, increment or decrement the indices based on the direction
        index1 += step1
        index2 += step2

    return result_list


def process_sequences(file_path):
    sequences = parse_yop(file_path)
    # Initialize lists and variables to store results and track axis limits
    result_sequences = []# List to store processed sequences
    directions = []# List to store direction information for each sequence
    x_label, y_label = 'X-axis', 'Y-axis'# Default axis labels

    # Initialize variables to track the minimum and maximum values for x and y axes
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')

    # Variables to track the maximum values for A and B sequences
    Amax, Bmax = 0, 0
    # Loop through each sequence in the parsed sequences list
    for i, sequence in tqdm(enumerate(sequences), total=len(sequences), desc="Processing sequences"):
        # Extract fields from the current sequence
        fields = extract_fields(sequence)
        # If fields cannot be extracted (None is returned), skip this sequence
        if fields is None:
            print(f"Sequence {i + 1} has issues with extracting fields")
            continue
        # For the first sequence, extract and set the x and y axis labels
        if i == 0:
            x_label, y_label = fields['x_label'], fields['y_label']
        
        # Generate a list of (x, y, intensity) tuples for the sequence
        result_list = generate_list(fields)
        if not result_list:  # If result_list is empty, skip the updates
            continue
        # Append the processed result list to the result_sequences list
        result_sequences.append(result_list)
        # Append the result list along with its direction to the directions list
        directions.append((result_list, fields['direction']))

        # Unpack the start and end positions from the fields for updating axis limits
        start1, end1, start2, end2 = fields['indexes']
        Amax = max(Amax, start1, end1)# Update Amax to the maximum value seen so far in the A sequence
        Bmax = max(Bmax, start2, end2) # Update Bmax to the maximum value seen so far in the B sequence

        # Update the axis limits based on the values in the result list
        for x, y, _ in result_list:
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y
    # Determine if the plot should be inverted based on the comparison of Amax and Bmax
    inverted = Amax < Bmax

    # Check if axis limits were updated; if not, return None for all values
    if min_x == float('inf') or max_x == float('-inf') or min_y == float('inf') or max_y == float('-inf'):
        return None, None, None, None, None, None, x_label, y_label, inverted
    # Return the processed sequences, directions, and axis limits along with the labels and inversion flag
    return result_sequences, directions, min_x, max_x, min_y, max_y, x_label, y_label, inverted
