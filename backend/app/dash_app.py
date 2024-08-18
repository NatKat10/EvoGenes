

import dash
from dash import dcc, html
from dash.dependencies import Input, Output,State
import plotly.graph_objects as go
import requests
import logging
logging.basicConfig(level=logging.INFO)
import time
import random

# Function to create the Dash application and integrate it with the Flask app
def create_dash_app(flask_app):
    # Initialize the Dash app with the Flask server and base URL
    dash_app = dash.Dash(
        __name__,
        server=flask_app,
        url_base_pathname='/dash/',
        suppress_callback_exceptions=True
    )
    # Function to create a gene plot based on exon intervals
    def create_gene_plot(exon_intervals, marker_pos=[], marker_heights=[], marker_colors=[], x_range=None, is_vertical=False, return_range=False):
        # Return an empty figure if no exon intervals are provided
        if not exon_intervals:
            return go.Figure()
        
        # Determine the minimum start and maximum end of the exons
        min_start = min(start for start, _ in exon_intervals)
        max_end = max(end for _, end in exon_intervals)

        # Set the x-axis range to the exon range if not provided
        if x_range is None:
            x_range = [min_start, max_end]

        # Trace for exon regions
        exon_x = []
        exon_y = []
        for start, end in exon_intervals:
            exon_x.extend([start, start, end, end, None])
            exon_y.extend([0, 0.5, 0.5, 0, None])# Intron line positioned between exons

        exon_trace = go.Scatter(x=exon_x, y=exon_y, mode='lines', fill='tozeroy', fillcolor='black',
                                line=dict(width=0), opacity=0.6, showlegend=False)

        # Create an intron line that spans the entire x-axis range
        intron_x = [x_range[0], x_range[1], None]
        intron_y = [0.25, 0.25, None]  # Use a constant y-value below the exon regions
        # Trace for intron regions (connecting exons)
        intron_trace = go.Scattergl(x=intron_x, y=intron_y, mode='lines', line=dict(color='black', width=1, dash='solid'),
                                    opacity=0.6, showlegend=False)
        # Trace for any markers (e.g., mutations or features of interest)
        marker_trace = go.Scattergl(x=marker_pos, y=[y + 0.5 for y in marker_heights], mode='markers',
                                    marker=dict(size=8, color=marker_colors, opacity=1), showlegend=False)
        # Combine all traces into the data list
        data = [exon_trace, intron_trace, marker_trace]
        # Configure the layout of the plot
        layout = go.Layout(
            width=780 if not is_vertical else 550,
            height=90,
            xaxis=dict(
                showgrid=False, 
                range=x_range,
                side='bottom' if is_vertical else 'top',# Position of the x-axis labels
                tickangle=-90 if is_vertical else 0,# Rotate labels for vertical plots
            ),
            yaxis=dict(
                showgrid=False,
                showticklabels=False,
                range=[-0.1, 0.6],  # Ensure this range accommodates both exons and introns
                fixedrange=True,
                zeroline=False,
                side='left' if is_vertical else 'right'
            ),
            margin=dict(l=60, r=55, t=5, b=35) if is_vertical else dict(l=40, r=5, t=5, b=35),
            hovermode='closest'
        )
        # Create the figure with the data and layout
        fig = go.Figure(data=data, layout=layout)
        fig.update_xaxes(nticks=10)

        if return_range:
            return fig, x_range
        else:
            return fig


    # Function to create a dot plot showing gene similarities
    def plot_dotplot(directions, min_x, max_x, min_y, max_y, x_label, y_label, sampling_fraction='0.1', inverted=False):
        logging.info("Start processing plot_dotplot function")
        start_time = time.time()
        # Lists to store coordinates and colors for forward and reverse directions
        x_vals_f, y_vals_f, colors_f = [], [], []
        x_vals_r, y_vals_r, colors_r = [], [], []
        # Color map for different levels of intensity and direction
        color_map = {
            'f': {1: 'rgba(204, 255, 204, 0.6)', 2: 'rgba(102, 204, 102, 0.6)', 3: 'rgba(0, 153, 0, 0.6)'},
            'r': {1: 'rgba(255, 204, 204, 0.6)', 2: 'rgba(204, 102, 102, 0.6)', 3: 'rgba(153, 0, 0, 0.6)'}
        }

        total_directions = len(directions)
        logging.info(f"Total directions: {total_directions}")
        # If sampling all data and there are more than 40,000 directions, reduce to 40%
        if sampling_fraction == 'all' and total_directions > 40000:
            sampling_fraction = 0.4  # Show only 40% of the dots
            logging.info("Sampling 40% of the dots due to large number of directions and 'all' sampling fraction selected")
        
        # Separate coordinates into forward and reverse directions
        for seq_list, direction in directions:
            for x, y, intensity in seq_list:
                color = color_map[direction][intensity]
                if inverted:
                    x, y = y, x
                if direction == 'f':
                    x_vals_f.append(x)
                    y_vals_f.append(y)
                    colors_f.append(color)
                else:
                    x_vals_r.append(x)
                    y_vals_r.append(y)
                    colors_r.append(color)

        logging.info(f"Forward points: {len(x_vals_f)}, Reverse points: {len(x_vals_r)}")
        # Function to randomly sample data points
        def sample_data(x_vals, y_vals, colors, sample_fraction):
            sample_size = int(len(x_vals) * sample_fraction)
            sampled_indices = random.sample(range(len(x_vals)), sample_size)
            return (
                [x_vals[i] for i in sampled_indices],
                [y_vals[i] for i in sampled_indices],
                [colors[i] for i in sampled_indices]
            )
        # If sampling is not 'all' or 100%, apply sampling to data points
        if sampling_fraction != 'all' and sampling_fraction != '1.0':
            sampling_fraction = float(sampling_fraction)
            x_vals_f, y_vals_f, colors_f = sample_data(x_vals_f, y_vals_f, colors_f, sampling_fraction)
            x_vals_r, y_vals_r, colors_r = sample_data(x_vals_r, y_vals_r, colors_r, sampling_fraction)

        logging.info(f"Sampled Forward points: {len(x_vals_f)}, Sampled Reverse points: {len(x_vals_r)}")
        # Create traces for forward and reverse directions
        traces = []

        if x_vals_f:
            traces.append(go.Scattergl(
                x=x_vals_f, y=y_vals_f, mode='markers',
                marker=dict(color=colors_f, size=2), name='Forward'
            ))
        if x_vals_r:
            traces.append(go.Scattergl(
                x=x_vals_r, y=y_vals_r, mode='markers',
                marker=dict(color=colors_r, size=2), name='Reverse'
            ))
        # Configure the layout of the dot plot
        layout = go.Layout(
            width=780,
            height=550,
            title='Dot Plot of Gene Similarities',
            xaxis=dict(title=x_label, range=[min_x, max_x], showgrid=False),
            yaxis=dict(title=y_label, range=[max_y, min_y], showgrid=False, showticklabels=True, side='right'),
            hovermode='closest',
            legend=dict(
                x=1,
                y=1.1,
                xanchor='right',
                yanchor='top',
                orientation='h'
            ),
            margin=dict(l=5, r=5, t=60, b=35)
        )

        

        end_time = time.time()
        logging.info(f"Completed processing plot_dotplot function in {end_time - start_time:.2f} seconds")
        # Create the figure and set the number of ticks on the axes
        fig = go.Figure(data=traces, layout=layout)
        fig.update_yaxes(nticks=10)
        fig.update_xaxes(nticks=10)


        return fig


    dash_app.layout = html.Div([
        # Graph component for displaying the gene plot, initialized with an empty figure
        dcc.Graph(id='gene-plot', figure=create_gene_plot([])),
        dcc.Graph(id='dotplot'),
        dcc.Store(id='dotplot-data', data=None),
        dcc.Store(id='relayout-data', data=None)
    ])

    @dash_app.callback(
        Output('relayout-data', 'data'),
        [Input('dotplot', 'relayoutData')],
        [State('relayout-data', 'data')]
    )
    def capture_zoom_event(relayout_data, existing_relayout_data):
        # Check if there is new relayout data (e.g., from a zoom or pan event)
        if relayout_data:
            # Initialize or update the existing relayout data with the new data
            existing_relayout_data = existing_relayout_data or {}
            existing_relayout_data.update(relayout_data)
            # Send the updated relayout data to the backend server for processing
            requests.post(f'{flask_app.config["SERVER_NAME"]}/dash/relayout', json=relayout_data)
        return existing_relayout_data

    return dash_app, create_gene_plot, plot_dotplot