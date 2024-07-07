

import dash
from dash import dcc, html
from dash.dependencies import Input, Output,State
import plotly.graph_objects as go
import requests
import logging
logging.basicConfig(level=logging.INFO)
import time
import random


def create_dash_app(flask_app):
    dash_app = dash.Dash(
        __name__,
        server=flask_app,
        url_base_pathname='/dash/',
        suppress_callback_exceptions=True
    )

    def create_gene_plot(exon_intervals, marker_pos=[], marker_heights=[], marker_colors=[], x_range=None):
        # This function creates a Plotly figure for visualizing gene structures.
        if not exon_intervals:
            return go.Figure()

        # exon_intervals: List of exon intervals for plotting.
        # marker_pos, marker_heights, marker_colors: Optional lists for adding markers to the plot.
        # x_range: Optional range for the x-axis. If exon_intervals is empty, it returns an empty figure.
        min_start = min(start for start, _ in exon_intervals)
        max_end = max(end for _, end in exon_intervals)
        # minimum start and maximum end positions of the exons in the intervals.

        # Directly use the provided x_range if available
        if x_range is None:
            x_range = [min_start, max_end]

        # These lists are created for plotting exon intervals.
        exon_x = []  # This list stores x-coordinates for exon plotting
        exon_y = []  # This list stores y-coordinates for exon plotting
        for start, end in exon_intervals:
            exon_x.extend([start, start, end, end, None])
            exon_y.extend([0, 0.5, 0.5, 0, None])

        exon_trace = go.Scatter(x=exon_x, y=exon_y, mode='lines', fill='tozeroy', fillcolor='black',  # This is a Plotly Scatter trace for the exons.
                                line=dict(width=0), opacity=0.6, showlegend=False)

        intron_x = []
        intron_y = []
        for i in range(len(exon_intervals) - 1):
            start = exon_intervals[i][1]
            end = exon_intervals[i + 1][0]
            mid_x = (start + end) / 2
            mid_y = 0.25
            intron_x.extend([start, mid_x, None, mid_x, end, None])
            intron_y.extend([mid_y, 0.5, None, 0.5, mid_y, None])

        intron_trace = go.Scattergl(x=intron_x, y=intron_y, mode='lines', line=dict(color='grey', width=2, dash='solid'),  # This is a Plotly Scatter trace for the introns.
                                    opacity=0.6, showlegend=False)

        marker_trace = go.Scattergl(x=marker_pos, y=[y + 0.5 for y in marker_heights], mode='markers',
                                    marker=dict(size=8, color=marker_colors, opacity=1), showlegend=False)

        data = [exon_trace, intron_trace, marker_trace]

        layout = go.Layout(
            width=800,
            height=70,
            xaxis=dict(title='Genomic Position', showgrid=True, range=x_range),
            yaxis=dict(showgrid=False, showticklabels=False, range=[-0.1, 0.6], fixedrange=True),
            margin=dict(l=5, r=5, t=5, b=35),
            hovermode='closest'
        )

        fig = go.Figure(data=data, layout=layout)
        return fig

    def plot_dotplot(directions, min_x, max_x, min_y, max_y, x_label, y_label, sampling_fraction='0.1', inverted=False):
        logging.info("Start processing plot_dotplot function")
        start_time = time.time()
        x_vals_f, y_vals_f, colors_f = [], [], []
        x_vals_r, y_vals_r, colors_r = [], [], []

        color_map = {
            'f': {1: 'rgba(204, 255, 204, 0.6)', 2: 'rgba(102, 204, 102, 0.6)', 3: 'rgba(0, 153, 0, 0.6)'},
            'r': {1: 'rgba(255, 204, 204, 0.6)', 2: 'rgba(204, 102, 102, 0.6)', 3: 'rgba(153, 0, 0, 0.6)'}
        }

        total_directions = len(directions)
        logging.info(f"Total directions: {total_directions}")

        if sampling_fraction == 'all' and total_directions > 40000:
            sampling_fraction = 0.4  # Show only 40% of the dots
            logging.info("Sampling 40% of the dots due to large number of directions and 'all' sampling fraction selected")

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

        def sample_data(x_vals, y_vals, colors, sample_fraction):
            sample_size = int(len(x_vals) * sample_fraction)
            sampled_indices = random.sample(range(len(x_vals)), sample_size)
            return (
                [x_vals[i] for i in sampled_indices],
                [y_vals[i] for i in sampled_indices],
                [colors[i] for i in sampled_indices]
            )

        if sampling_fraction != 'all' and sampling_fraction != '1.0':
            sampling_fraction = float(sampling_fraction)
            x_vals_f, y_vals_f, colors_f = sample_data(x_vals_f, y_vals_f, colors_f, sampling_fraction)
            x_vals_r, y_vals_r, colors_r = sample_data(x_vals_r, y_vals_r, colors_r, sampling_fraction)

        logging.info(f"Sampled Forward points: {len(x_vals_f)}, Sampled Reverse points: {len(x_vals_r)}")

        traces = []

        if x_vals_f:
            traces.append(go.Scattergl(
                x=x_vals_f, y=y_vals_f, mode='markers',
                marker=dict(color=colors_f, size=5), name='Forward'
            ))
        if x_vals_r:
            traces.append(go.Scattergl(
                x=x_vals_r, y=y_vals_r, mode='markers',
                marker=dict(color=colors_r, size=5), name='Reverse'
            ))

        layout = go.Layout(
            width=800,
            height=500,
            title='Dot Plot of Gene Similarities',
            xaxis=dict(title=x_label, range=[min_x, max_x], showgrid=False),
            yaxis=dict(title=y_label, range=[max_y, min_y], showgrid=False, showticklabels=True, side='right'),  # Set range explicitly
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
        return go.Figure(data=traces, layout=layout)


    dash_app.layout = html.Div([
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
        if relayout_data:
            existing_relayout_data = existing_relayout_data or {}
            existing_relayout_data.update(relayout_data)
            # Send the relayout data to the backend
            requests.post(f'{flask_app.config["SERVER_NAME"]}/dash/relayout', json=relayout_data)
        return existing_relayout_data

    return dash_app, create_gene_plot, plot_dotplot