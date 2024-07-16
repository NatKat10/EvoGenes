import re
import sys
# import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm  # for progress bar
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import plotly.graph_objs as go

# # from dash import dcc
# # from dash import html

# # from backend.app import dash_app


# def parse_yop(file_path):
#     sequences = []
#     current_sequence = []

#     # Regular expression to match the start of a sequence
#     sequence_start_pattern = re.compile(r"^\*\((\d+)-(\d+)\)\((\d+)-(\d+)\) Ev: \S+ s: \d+/\d+ [fr]")

#     with open(file_path, 'r', encoding='utf-8') as file:
#         for line in file:#reading each line in the yop file.
#             if sequence_start_pattern.match(line):# if the line matches the start pattern
#                 if current_sequence:
#                     sequences.append(current_sequence)
#                     current_sequence = []
#             current_sequence.append(line.strip())

#         if current_sequence:# puts all the lines that related to single sequance and making a list of sequances
#             sequences.append(current_sequence)

#     return sequences #Returns a list of sequences

# def extract_fields(sequence):
#     fields = {}

#     # Extract the indexes and direction from the first line
#     first_line = sequence[0]
#     match = re.match(r"^\*\((\d+)-(\d+)\)\((\d+)-(\d+)\) Ev: \S+ s: \d+/\d+ ([fr])", first_line)#check if the first line indid matches the beggining pattern.
#     if not match:
#         return None

#     start1, end1, start2, end2, direction = match.groups()#extracting the needed fields " (25136-25194)(29160-29218) Ev: 0.000135011 s: 59/59 f "
#     fields['indexes'] = (int(start1), int(end1), int(start2), int(end2))
#     fields['direction'] = direction

#     # Extract axis labels from the second line
#     second_line = sequence[1]
#     labels_match = re.match(r'^\* "([^"]+)" \(\d+ bp\) / "([^"]+)" \(\d+ bp\)', second_line)
#     if labels_match:
#         fields['x_label'], fields['y_label'] = labels_match.groups()
#     else:
#         fields['x_label'], fields['y_label'] = 'X-axis', 'Y-axis'

#     # Extract the line with the mutation symbols
#     mutation_line = None
#     for line in sequence:
#         line_content = line.strip()
#         # Check if the line contains only mutation symbols and no alphanumeric characters
#         if re.fullmatch(r'[|:. ]+', line_content):
#             mutation_line = line_content
#             break

#     if mutation_line is None:
#         return None
#     fields['mutation_line'] = mutation_line

#     return fields # returning only the needed fields for the dotplot creation (2 start, 2 end, direction, labels and the mutation line)

# def generate_list(fields):#Generates a list of tuples (index1, index2, intensity) based on the mutation symbols.
#     start1, end1, start2, end2 = fields['indexes']# get the fields we need
#     mutation_line = fields['mutation_line']

#     result_list = []
#     if fields['direction'] == 'f':# in case the direction is farward we start from beggining and going up 
#         index1, index2 = start1, start2
#         step = 1
#     else:
#         index1, index2 = start1, start2#in case the direction is reverse we do the same but in the opposite direction
#         step = -1

#     for char in mutation_line:
#         if char == ' ':
#             index1 += step
#             index2 += step
#             continue
#         elif char == '|':
#             result_list.append((index1, index2, 3)) # if the aligment result is "match" we give the highest score etc.
#         elif char == ':':
#             result_list.append((index1, index2, 2))
#         elif char == '.':
#             result_list.append((index1, index2, 1))

#         index1 += step
#         index2 += step

#     return result_list

# def process_sequences(file_path):
#     sequences = parse_yop(file_path)
    
#     result_sequences = []
#     directions = []
#     x_label, y_label = 'X-axis', 'Y-axis'

#     # Variables to store the axis limits
#     min_x = float('inf')
#     max_x = float('-inf')
#     min_y = float('inf')
#     max_y = float('-inf')

#     for i, sequence in tqdm(enumerate(sequences), total=len(sequences), desc="Processing sequences"):
#         fields = extract_fields(sequence)
#         if fields is None:
#             print(f"Sequence {i + 1} has issues with extracting fields")
#             continue

#         if i == 0:  # Assume all sequences have the same labels
#             x_label, y_label = fields['x_label'], fields['y_label']

#         result_list = generate_list(fields)
#         result_sequences.append(result_list)
#         directions.append((result_list, fields['direction']))

#         # Update axis limits
#         for x, y, _ in result_list:# updating the min and max for the dotplot according to the results 
#             if x < min_x:
#                 min_x = x
#             if x > max_x:
#                 max_x = x
#             if y < min_y:
#                 min_y = y
#             if y > max_y:
#                 max_y = y
#     return result_sequences, directions, min_x, max_x, min_y, max_y, x_label, y_label

# def plot_dotplot(yop_path, output_path):
#     result_sequences, directions, min_x, max_x, min_y, max_y, x_label, y_label = process_sequences(yop_path)#Processes the YOP file to get sequences and directions.

#     # Print results for debugging
#     print("Finished processing sequences.")
#     print(f"Number of sequences processed: {len(result_sequences)}")

#     # Check if there is any data to plot
#     if not result_sequences or not directions:
#         print("No data to plot.")
#         return
    
#     print(f"Plotting {len(result_sequences)} sequences.")
    

#     x_vals_f, y_vals_f, colors_f = [], [], []
#     x_vals_r, y_vals_r, colors_r = [], [], []

#     # Updated color map
#     color_map = {
#         'f': {1: (0.8, 1.0, 0.8), 2: (0.4, 0.8, 0.4), 3: (0.0, 0.6, 0.0)},
#         'r': {1: (1.0, 0.8, 0.8), 2: (0.8, 0.4, 0.4), 3: (0.6, 0.0, 0.0)}
#     }

#     for seq_list, direction in directions:
#         for x, y, intensity in seq_list:
#             if direction == 'f':
#                 x_vals_f.append(x)
#                 y_vals_f.append(y)
#                 colors_f.append(color_map[direction][intensity])
#             else:
#                 x_vals_r.append(x)
#                 y_vals_r.append(y)
#                 colors_r.append(color_map[direction][intensity])


#     # Plot the dot plot in batches
#     fig, ax = plt.subplots(figsize=(10, 10))

#     dot_size = 10  # Increase dot size

#     line_length = 20  # Length of the lines

#     # if x_vals['f']:
#     #     ax.hlines(y=y_vals['f'], xmin=[x for x in x_vals['f']], xmax=[x + line_length for x in x_vals['f']], colors=colors['f'], alpha=0.6, label='forward')
#     # if x_vals['r']:
#     #     ax.hlines(y=y_vals['r'], xmin=[x for x in x_vals['r']], xmax=[x + line_length for x in x_vals['r']], colors=colors['r'], alpha=0.6, label='reverse')

#     if x_vals_f:
#         ax.hlines(y=y_vals_f, xmin=np.array(x_vals_f), xmax=np.array(x_vals_f) + line_length, colors=colors_f, alpha=0.6, label='forward')
#     if x_vals_r:
#         ax.hlines(y=y_vals_r, xmin=np.array(x_vals_r) - line_length, xmax=np.array(x_vals_r), colors=colors_r, alpha=0.6, label='reverse')


#     tick_interval = 5000
#     axis_min = min(min_x, min_y)
#     axis_max = max(max_x, max_y)

#     # ax.set_xlim(axis_min, axis_max)
#     # ax.set_ylim(axis_max, axis_min) 

#     axis_min = (axis_min // tick_interval) * tick_interval
#     axis_max = ((axis_max + tick_interval - 1) // tick_interval) * tick_interval

#     ax.set_xlim(axis_min, axis_max)
#     ax.set_ylim(axis_max, axis_min)

#     ax.set_xlabel(x_label)
#     ax.set_ylabel(y_label)
#     ax.set_title('Dot Plot of Gene Similarities')
#     ax.yaxis.tick_right()  # Move the Y-axis to the right
#     ax.yaxis.set_label_position("right")
#     ax.legend()
#     ax.grid(False)


#     x_ticks = np.arange(axis_min, axis_max + tick_interval, tick_interval)
#     y_ticks = np.arange(axis_min, axis_max + tick_interval, tick_interval)
#     ax.set_xticks(x_ticks)
#     ax.set_yticks(y_ticks)

#     ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
#     ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))

#     plt.xticks(rotation=90)  # Rotate X-axis labels to prevent overlap



#     plt.savefig(output_path, dpi=150)  # Reduced DPI for quicker rendering
#     print(f"Plot saved as '{output_path}'.")
#     # plt.show()
#     print("Plot displayed.")



# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python yop_reader.py <input_yop_path> <output_image_path>")
#         sys.exit(1)

#     yop_path = sys.argv[1]
#     output_path = sys.argv[2]

#     plot_dotplot(yop_path, output_path)


def parse_yop(file_path):
    sequences = []
    current_sequence = []

    # Pre-compiled regular expression to match the start of a sequence
    sequence_start_pattern = re.compile(r"^\*\((\d+)-(\d+)\)\((\d+)-(\d+)\) Ev: \S+ s: \d+/\d+ [fr]")

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if sequence_start_pattern.match(line):
                if current_sequence:
                    sequences.append(current_sequence)
                    current_sequence = []
            current_sequence.append(line.strip())

        if current_sequence:
            sequences.append(current_sequence)

    return sequences

def extract_fields(sequence):
    fields = {}
    first_line = sequence[0]
    match = re.match(r"^\*\((\d+)-(\d+)\)\((\d+)-(\d+)\) Ev: \S+ s: \d+/\d+ ([fr])", first_line)
    if not match:
        return None

    start1, end1, start2, end2, direction = match.groups()
    fields['indexes'] = (int(start1), int(end1), int(start2), int(end2))
    fields['direction'] = direction

    second_line = sequence[1]
    labels_match = re.match(r'^\* "([^"]+)" \(\d+ bp\) / "([^"]+)" \(\d+ bp\)', second_line)
    if labels_match:
        fields['x_label'], fields['y_label'] = labels_match.groups()
    else:
        fields['x_label'], fields['y_label'] = 'X-axis', 'Y-axis'

    mutation_line = ''.join(line.strip() for line in sequence if re.fullmatch(r'[|:. ]+', line.strip()))

    if mutation_line is None:
        return None
    fields['mutation_line'] = mutation_line


    return fields

def generate_list(fields):
    start1, end1, start2, end2 = fields['indexes']
    mutation_line = fields['mutation_line']

    result_list = []
    if fields['direction'] == 'f':
        index1, index2 = start1, start2
        step1, step2 = 1, 1
    else:
        index1, index2 = start1, start2
        step1, step2 = -1, 1  # x decrements, y increments

    for char in mutation_line:
        if char == ' ':
            index1 += step1
            index2 += step2
            continue
        elif char == '|':
            result_list.append((index1, index2, 3))  
            result_list.append((index1, index2, 2))
        elif char == '.':
            result_list.append((index1, index2, 1))

        index1 += step1
        index2 += step2

    return result_list


def process_sequences(file_path):
    sequences = parse_yop(file_path)

    result_sequences = []
    directions = []
    x_label, y_label = 'X-axis', 'Y-axis'

    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')

    Amax, Bmax = 0, 0

    for i, sequence in tqdm(enumerate(sequences), total=len(sequences), desc="Processing sequences"):
        fields = extract_fields(sequence)
        if fields is None:
            print(f"Sequence {i + 1} has issues with extracting fields")
            continue

        if i == 0:
            x_label, y_label = fields['x_label'], fields['y_label']

        result_list = generate_list(fields)
        if not result_list:  # If result_list is empty, skip the updates
            continue

        result_sequences.append(result_list)
        directions.append((result_list, fields['direction']))

        start1, end1, start2, end2 = fields['indexes']
        Amax = max(Amax, start1, end1)
        Bmax = max(Bmax, start2, end2)

        # Update axis limits
        for x, y, _ in result_list:
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

    inverted = Amax < Bmax

    # Check if axis limits were updated
    if min_x == float('inf') or max_x == float('-inf') or min_y == float('inf') or max_y == float('-inf'):
        return None, None, None, None, None, None, x_label, y_label, inverted

    return result_sequences, directions, min_x, max_x, min_y, max_y, x_label, y_label, inverted
