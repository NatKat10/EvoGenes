import re #for parsing the yop file 
import matplotlib.pyplot as plt #for plotting the dotplot
from tqdm import tqdm  # for progress bar
import sys

def parse_yop(file_path):
    sequences = []
    current_sequence = []

    # Regular expression to match the start of a sequence
    sequence_start_pattern = re.compile(r"^\*\((\d+)-(\d+)\)\((\d+)-(\d+)\) Ev: \S+ s: \d+/\d+ [fr]")

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:#reading each line in the yop file.
            if sequence_start_pattern.match(line):# if the line matches the start pattern
                if current_sequence:
                    sequences.append(current_sequence)
                    current_sequence = []
            current_sequence.append(line.strip())

        if current_sequence:# puts all the lines that related to single sequance and making a list of sequances
            sequences.append(current_sequence)

    return sequences #Returns a list of sequences

def extract_fields(sequence):
    fields = {}

    # Extract the indexes and direction from the first line
    first_line = sequence[0]
    match = re.match(r"^\*\((\d+)-(\d+)\)\((\d+)-(\d+)\) Ev: \S+ s: \d+/\d+ ([fr])", first_line)#check if the first line indid matches the beggining pattern.
    if not match:
        return None

    start1, end1, start2, end2, direction = match.groups()#extracting the needed fields " (25136-25194)(29160-29218) Ev: 0.000135011 s: 59/59 f "
    fields['indexes'] = (int(start1), int(end1), int(start2), int(end2))
    fields['direction'] = direction

    # Extract axis labels from the second line
    second_line = sequence[1]
    labels_match = re.match(r'^\* "([^"]+)" \(\d+ bp\) / "([^"]+)" \(\d+ bp\)', second_line)
    if labels_match:
        fields['x_label'], fields['y_label'] = labels_match.groups()
    else:
        fields['x_label'], fields['y_label'] = 'X-axis', 'Y-axis'

    # Extract the line with the mutation symbols
    mutation_line = None
    for line in sequence:
        line_content = line.strip()
        # Check if the line contains only mutation symbols and no alphanumeric characters
        if re.fullmatch(r'[|:. ]+', line_content):
            mutation_line = line_content
            break

    if mutation_line is None:
        return None
    fields['mutation_line'] = mutation_line

    return fields # returning only the needed fields for the dotplot creation (2 start, 2 end, direction, labels and the mutation line)

def generate_list(fields):#Generates a list of tuples (index1, index2, intensity) based on the mutation symbols.
    start1, end1, start2, end2 = fields['indexes']# get the fields we need
    mutation_line = fields['mutation_line']

    result_list = []
    if fields['direction'] == 'f':# in case the direction is farward we start from beggining and going up 
        index1, index2 = start1, start2
        step = 1
    else:
        index1, index2 = start1, start2#in case the direction is reverse we do the same but in the opposite direction
        step = -1

    for char in mutation_line:
        if char == ' ':
            continue
        elif char == '|':
            result_list.append((index1, index2, 3)) # if the aligment result is "match" we give the highest score etc.
        elif char == ':':
            result_list.append((index1, index2, 2))
        elif char == '.':
            result_list.append((index1, index2, 1))

        index1 += step
        index2 += step

    return result_list

def process_sequences(file_path):
    sequences = parse_yop(file_path)
    
    result_sequences = []
    directions = []
    x_label, y_label = 'X-axis', 'Y-axis'

    # Variables to store the axis limits
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')

    for i, sequence in tqdm(enumerate(sequences), total=len(sequences), desc="Processing sequences"):
        fields = extract_fields(sequence)
        if fields is None:
            print(f"Sequence {i + 1} has issues with extracting fields")
            continue

        if i == 0:  # Assume all sequences have the same labels
            x_label, y_label = fields['x_label'], fields['y_label']

        result_list = generate_list(fields)
        result_sequences.append(result_list)
        directions.append((result_list, fields['direction']))

        # Update axis limits
        for x, y, _ in result_list:# updating the min and max for the dotplot according to the results 
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

    return result_sequences, directions, min_x, max_x, min_y, max_y, x_label, y_label

def plot_dotplot(yop_path, output_path):
    result_sequences, directions, min_x, max_x, min_y, max_y, x_label, y_label = process_sequences(yop_path)#Processes the YOP file to get sequences and directions.

    # Print results for debugging
    print("Finished processing sequences.")
    print(f"Number of sequences processed: {len(result_sequences)}")

    # Check if there is any data to plot
    if not result_sequences or not directions:
        print("No data to plot.")
        return
    
    print(f"Plotting {len(result_sequences)} sequences.")
    
    # Prepare data for batch plotting
    x_vals = {'f': [], 'r': []}#putting the x values in the correct direction to know which color to use.
    y_vals = {'f': [], 'r': []}
    colors = {'f': [], 'r': []}

    # Updated color map
    color_map = {
        'f': {1: (0.8, 1.0, 0.8), 2: (0.4, 0.8, 0.4), 3: (0.0, 0.6, 0.0)},
        'r': {1: (1.0, 0.8, 0.8), 2: (0.8, 0.4, 0.4), 3: (0.6, 0.0, 0.0)}
    }

    for seq_list, direction in directions:
        for x, y, intensity in seq_list:
            x_vals[direction].append(x)
            y_vals[direction].append(y)
            colors[direction].append(color_map[direction][intensity])

    # Plot the dot plot in batches
    fig, ax = plt.subplots(figsize=(10, 10))

    dot_size = 5  # Increase dot size

    if x_vals['f']:#Creates a scatter plot with different colors and sizes based on the direction and intensity.
        ax.scatter(x_vals['f'], y_vals['f'], c=colors['f'], s=dot_size, label='forward', alpha=0.6, edgecolors='none')
    if x_vals['r']:
        ax.scatter(x_vals['r'], y_vals['r'], c=colors['r'], s=dot_size, label='reverse', alpha=0.6, edgecolors='none')

    # Set axis limits based on extracted indexes
    print(f"Setting axis limits: X({min_x}, {max_x}), Y({min_y}, {max_y})")
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
 
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title('Dot Plot of Gene Similarities')
    ax.legend()
    ax.grid(False)

    plt.savefig(output_path, dpi=150)  # Reduced DPI for quicker rendering
    print(f"Plot saved as '{output_path}'.")
    # plt.show()
    print("Plot displayed.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python yop_reader.py <input_yop_path> <output_image_path>")
        sys.exit(1)

    yop_path = sys.argv[1]
    output_path = sys.argv[2]

    plot_dotplot(yop_path, output_path)
