# import dash
# from dash import dcc, html
# from dash.dependencies import Input, Output
# import plotly.graph_objects as go

# def create_dash_app(flask_app):
#     dash_app = dash.Dash(
#         __name__,
#         server=flask_app,
#         url_base_pathname='/dash/'
#     )

#     def create_gene_plot(exon_intervals, marker_pos=[], marker_heights=[], marker_colors=[], x_range=None):
#         if not exon_intervals:
#             return go.Figure()

#         min_start = min(start for start, _ in exon_intervals)
#         max_end = max(end for _, end in exon_intervals)
#         x_indentation = 500

#         if x_range is None:
#             x_range = [min_start - x_indentation, max_end + x_indentation]
#         # else:
#         #     x_range_with_indentation = [x_range[0] + x_indentation, x_range[1] - x_indentation]

#         exon_x = []
#         exon_y = []
#         for start, end in exon_intervals:
#             exon_x.extend([start, start, end, end, None])
#             exon_y.extend([0, 0.5, 0.5, 0, None])

#         exon_trace = go.Scatter(x=exon_x, y=exon_y, mode='lines', fill='tozeroy', fillcolor='black',
#                                 line=dict(width=0), opacity=0.6, showlegend=False)

#         intron_x = []
#         intron_y = []
#         for i in range(len(exon_intervals) - 1):
#             start = exon_intervals[i][1]
#             end = exon_intervals[i + 1][0]
#             mid_x = (start + end) / 2
#             mid_y = 0.25
#             intron_x.extend([start, mid_x, None, mid_x, end, None])
#             intron_y.extend([mid_y, 0.5, None, 0.5, mid_y, None])

#         intron_trace = go.Scatter(x=intron_x, y=intron_y, mode='lines', line=dict(color='grey', width=2, dash='solid'),
#                                   opacity=0.6, showlegend=False)

#         marker_trace = go.Scatter(x=marker_pos, y=[y + 0.5 for y in marker_heights], mode='markers',
#                                   marker=dict(size=8, color=marker_colors, opacity=1), showlegend=False)

#         data = [exon_trace, intron_trace, marker_trace]

#         layout = go.Layout(
#             width=780,
#             height=70,
#             xaxis=dict(title='Genomic Position', showgrid=True, range=x_range),
#             yaxis=dict(showgrid=False, showticklabels=False, range=[-0.1, 0.6],fixedrange=True),
#             margin=dict(l=5, r=5, t=5, b=35),
#             # margin=dict(l=0, r=0, t=0, b=20),
#             # paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
#             # plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
#             hovermode='closest'
#         )

#         # config = {
#         #     # 'displayModeBar': True,
#         #     # 'modeBarButtonsToRemove': ['toImage'],
#         #     'displaylogo': False,
#         #     # 'modeBarButtonsToAdd': ['drawopenpath', 'eraseshape'],
#         #     # 'toImageButtonOptions': {
#         #     #     'format': 'svg',
#         #     #     'filename': 'custom_image',
#         #     #     'height': 800,
#         #     #     'width': 800,
#         #     #     'scale': 1
#         #     # },
#         #     # 'modeBarButtons': [['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'drawopenpath', 'eraseshape']],
#         #     # 'scrollZoom': True
#         # }

#         fig = go.Figure(data=data, layout=layout)
#         # fig.update_layout(modebar_orientation='h', modebar=dict(orientation='v', yanchor='bottom', y=0.01))
#         # fig.update_layout(config=config)

#         return fig
    
#     def plot_dotplot(directions, min_x, max_x, min_y, max_y, x_label, y_label):
#         x_vals_f, y_vals_f, colors_f = [], [], []
#         x_vals_r, y_vals_r, colors_r = [], [],[]

#         color_map = {
#             'f': {1: (0.8, 1.0, 0.8), 2: (0.4, 0.8, 0.4), 3: (0.0, 0.6, 0.0)},
#             'r': {1: (1.0, 0.8, 0.8), 2: (0.8, 0.4, 0.4), 3: (0.6, 0.0, 0.0)}
#         }

#         for seq_list, direction in directions:
#             for x, y, intensity in seq_list:
#                 if direction == 'f':
#                     x_vals_f.append(x)
#                     y_vals_f.append(y)
#                     colors_f.append(f'rgba{color_map[direction][intensity] + (0.6,)}')
#                 else:
#                     x_vals_r.append(x)
#                     y_vals_r.append(y)
#                     colors_r.append(f'rgba{color_map[direction][intensity] + (0.6,)}')

#         traces = []

#         if x_vals_f:
#             traces.append(go.Scatter(x=x_vals_f, y=y_vals_f, mode='markers', marker=dict(color=colors_f, size=5), name='Forward'))
#         if x_vals_r:
#             traces.append(go.Scatter(x=x_vals_r, y=y_vals_r, mode='markers', marker=dict(color=colors_r, size=5), name='Reverse'))

#         layout = go.Layout(
#             width=780,
#             title='Dot Plot of Gene Similarities',
#             xaxis=dict(title=x_label, range=[min_x, max_x], showgrid=False),
#             yaxis=dict(title=y_label, range=[max_y, min_y], showgrid=False, showticklabels=True,side='right'),
#             hovermode='closest',
#             legend=dict(
#                 x=1,
#                 y=1.1,
#                 xanchor='right',
#                 yanchor='top',
#                 orientation='h'
#             ),
#             margin=dict(l=5, r=5, t=60, b=35)
#         )

#         return go.Figure(data=traces, layout=layout)

#     dash_app.layout = html.Div([
#         dcc.Graph(id='gene-plot', figure=create_gene_plot([])),
#         dcc.Graph(id='dotplot'),
#         dcc.Store(id='dotplot-data', data=None)
    
#     ])

#     return dash_app, create_gene_plot, plot_dotplot

##### after normalizing the scale of gene structure to fit the dot plot

# import dash
# from dash import dcc, html
# from dash.dependencies import Input, Output
# import plotly.graph_objects as go

# def create_dash_app(flask_app):
#     dash_app = dash.Dash(
#         __name__,
#         server=flask_app,
#         url_base_pathname='/dash/'
#     )

#     def create_gene_plot(exon_intervals, marker_pos=[], marker_heights=[], marker_colors=[], x_range=None):
#         if not exon_intervals:
#             return go.Figure()

#         min_start = min(start for start, _ in exon_intervals)
#         max_end = max(end for _, end in exon_intervals)
#         x_indentation = 500

#         if x_range is None:
#             x_range = [min_start - x_indentation, max_end + x_indentation]
#         # else:
#         #     x_range_with_indentation = [x_range[0] + x_indentation, x_range[1] - x_indentation]

#         exon_x = []
#         exon_y = []
#         for start, end in exon_intervals:
#             exon_x.extend([start, start, end, end, None])
#             exon_y.extend([0, 0.5, 0.5, 0, None])

#         exon_trace = go.Scatter(x=exon_x, y=exon_y, mode='lines', fill='tozeroy', fillcolor='black',
#                                 line=dict(width=0), opacity=0.6, showlegend=False)

#         intron_x = []
#         intron_y = []
#         for i in range(len(exon_intervals) - 1):
#             start = exon_intervals[i][1]
#             end = exon_intervals[i + 1][0]
#             mid_x = (start + end) / 2
#             mid_y = 0.25
#             intron_x.extend([start, mid_x, None, mid_x, end, None])
#             intron_y.extend([mid_y, 0.5, None, 0.5, mid_y, None])

#         intron_trace = go.Scatter(x=intron_x, y=intron_y, mode='lines', line=dict(color='grey', width=2, dash='solid'),
#                                   opacity=0.6, showlegend=False)

#         marker_trace = go.Scatter(x=marker_pos, y=[y + 0.5 for y in marker_heights], mode='markers',
#                                   marker=dict(size=8, color=marker_colors, opacity=1), showlegend=False)

#         data = [exon_trace, intron_trace, marker_trace]

#         layout = go.Layout(
#             width=780,
#             height=70,
#             xaxis=dict(title='Genomic Position', showgrid=True, range=x_range),
#             yaxis=dict(showgrid=False, showticklabels=False, range=[-0.1, 0.6],fixedrange=True),
#             margin=dict(l=5, r=5, t=5, b=35),
#             # margin=dict(l=0, r=0, t=0, b=20),
#             # paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
#             # plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
#             hovermode='closest'
#         )

#         # config = {
#         #     # 'displayModeBar': True,
#         #     # 'modeBarButtonsToRemove': ['toImage'],
#         #     'displaylogo': False,
#         #     # 'modeBarButtonsToAdd': ['drawopenpath', 'eraseshape'],
#         #     # 'toImageButtonOptions': {
#         #     #     'format': 'svg',
#         #     #     'filename': 'custom_image',
#         #     #     'height': 800,
#         #     #     'width': 800,
#         #     #     'scale': 1
#         #     # },
#         #     # 'modeBarButtons': [['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'drawopenpath', 'eraseshape']],
#         #     # 'scrollZoom': True
#         # }

#         fig = go.Figure(data=data, layout=layout)
#         # fig.update_layout(modebar_orientation='h', modebar=dict(orientation='v', yanchor='bottom', y=0.01))
#         # fig.update_layout(config=config)

#         return fig
    
#     def plot_dotplot(directions, min_x, max_x, min_y, max_y, x_label, y_label):
#         x_vals_f, y_vals_f, colors_f = [], [], []
#         x_vals_r, y_vals_r, colors_r = [], [],[]

#         color_map = {
#             'f': {1: (0.8, 1.0, 0.8), 2: (0.4, 0.8, 0.4), 3: (0.0, 0.6, 0.0)},
#             'r': {1: (1.0, 0.8, 0.8), 2: (0.8, 0.4, 0.4), 3: (0.6, 0.0, 0.0)}
#         }

#         for seq_list, direction in directions:
#             for x, y, intensity in seq_list:
#                 if direction == 'f':
#                     x_vals_f.append(x)
#                     y_vals_f.append(y)
#                     colors_f.append(f'rgba{color_map[direction][intensity] + (0.6,)}')
#                 else:
#                     x_vals_r.append(x)
#                     y_vals_r.append(y)
#                     colors_r.append(f'rgba{color_map[direction][intensity] + (0.6,)}')

#         traces = []

#         if x_vals_f:
#             traces.append(go.Scatter(x=x_vals_f, y=y_vals_f, mode='markers', marker=dict(color=colors_f, size=5), name='Forward'))
#         if x_vals_r:
#             traces.append(go.Scatter(x=x_vals_r, y=y_vals_r, mode='markers', marker=dict(color=colors_r, size=5), name='Reverse'))

#         layout = go.Layout(
#             width=780,
#             title='Dot Plot of Gene Similarities',
#             xaxis=dict(title=x_label, range=[min_x, max_x], showgrid=False),
#             yaxis=dict(title=y_label, range=[max_y, min_y], showgrid=False, showticklabels=True,side='right'),
#             hovermode='closest',
#             legend=dict(
#                 x=1,
#                 y=1.1,
#                 xanchor='right',
#                 yanchor='top',
#                 orientation='h'
#             ),
#             margin=dict(l=5, r=5, t=60, b=35)
#         )

#         return go.Figure(data=traces, layout=layout)

#     dash_app.layout = html.Div([
#         dcc.Graph(id='gene-plot', figure=create_gene_plot([])),
#         dcc.Graph(id='dotplot'),
#         dcc.Store(id='dotplot-data', data=None)
    
#     ])

#     return dash_app, create_gene_plot, plot_dotplot

##### after normalizing the scale of gene structure to fit the dot plot

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

def create_dash_app(flask_app):
    #a function that takes a flask app instance as argument and
    #creates dash app
    dash_app = dash.Dash(
        __name__,
        server=flask_app,
        url_base_pathname='/dash/'
    )

    def create_gene_plot(exon_intervals, marker_pos=[], marker_heights=[], marker_colors=[], x_range=None):
        #This function creates a Plotly figure for visualizing gene structures.
        if not exon_intervals:
            return go.Figure()

        #exon_intervals: List of exon intervals for plotting.
        #marker_pos, marker_heights, marker_colors: Optional lists for adding markers to the plot.
        #x_range: Optional range for the x-axis. If exon_intervals is empty, it returns an empty figure.
        min_start = min(start for start, _ in exon_intervals)
        max_end = max(end for _, end in exon_intervals)
        #minimum start and maximum end positions of the exons in the intervals.
        
        # Adjusting to ensure the gene plot fits within the dot plot range
        if x_range is None:#If x_range is not provided, it sets the x-axis range to cover the entire gene length.
             #Otherwise, it adjusts x_range based on the provided range and gene length.
            x_range = [min_start, max_end]
        else:
            gene_length = max_end - min_start
            x_range = [x_range[0], x_range[0] + gene_length]


        #These lists are created for plotting exon intervals.
        exon_x = []#This list stores x-coordinates for exon plotting
        exon_y = []#This list stores y-coordinates for exon plotting
        for start, end in exon_intervals:
            exon_x.extend([start, start, end, end, None])
            exon_y.extend([0, 0.5, 0.5, 0, None])

        exon_trace = go.Scatter(x=exon_x, y=exon_y, mode='lines', fill='tozeroy', fillcolor='black',#This is a Plotly Scatter trace for the exons.
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

        intron_trace = go.Scatter(x=intron_x, y=intron_y, mode='lines', line=dict(color='grey', width=2, dash='solid'),#This is a Plotly Scatter trace for the introns.
                                  opacity=0.6, showlegend=False)

        marker_trace = go.Scatter(x=marker_pos, y=[y + 0.5 for y in marker_heights], mode='markers',
                                  marker=dict(size=8, color=marker_colors, opacity=1), showlegend=False)

        data = [exon_trace, intron_trace, marker_trace]

        layout = go.Layout(
            width=780,
            height=70,
            xaxis=dict(title='Genomic Position', showgrid=True, range=x_range),
            yaxis=dict(showgrid=False, showticklabels=False, range=[-0.1, 0.6], fixedrange=True),
            margin=dict(l=5, r=5, t=5, b=35),
            hovermode='closest'
        )

        fig = go.Figure(data=data, layout=layout)
        return fig

    def plot_dotplot(directions, min_x, max_x, min_y, max_y, x_label, y_label):
        x_vals_f, y_vals_f, colors_f = [], [], []# lists to store x and y values for forward (green)
        x_vals_r, y_vals_r, colors_r = [], [],[]#lists to store x and y values for reverse (red)

        color_map = {
            'f': {1: (0.8, 1.0, 0.8), 2: (0.4, 0.8, 0.4), 3: (0.0, 0.6, 0.0)},#defines the shades of green (darkest green is "|", lightest green is ".")
            'r': {1: (1.0, 0.8, 0.8), 2: (0.8, 0.4, 0.4), 3: (0.6, 0.0, 0.0)}#defines the shades of red (darkest red is "|", lightest red is ".")
        }

        for seq_list, direction in directions:# iterates over each sequence list and its direction
            for x, y, intensity in seq_list:#iterates over each sequence's x, y, and intensity values
                if direction == 'f':# if its farward (green) append the indexes aand the correct color shade
                    x_vals_f.append(x)
                    y_vals_f.append(y)
                    colors_f.append(f'rgba{color_map[direction][intensity] + (0.6,)}')
                else:
                    x_vals_r.append(x)#same for reverse(red)
                    y_vals_r.append(y)
                    colors_r.append(f'rgba{color_map[direction][intensity] + (0.6,)}')

        traces = []

        if x_vals_f:#Each point represents a pair of values for two variables.
            traces.append(go.Scatter(x=x_vals_f, y=y_vals_f, mode='markers', marker=dict(color=colors_f, size=5), name='Forward'))#plotting the x and y dots/maybe need to change from markers to lines 
        if x_vals_r:
            traces.append(go.Scatter(x=x_vals_r, y=y_vals_r, mode='markers', marker=dict(color=colors_r, size=5), name='Reverse'))

        layout = go.Layout(
            width=780,
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

        return go.Figure(data=traces, layout=layout)

    dash_app.layout = html.Div([#defines the layout of your Dash application
        dcc.Graph(id='gene-plot', figure=create_gene_plot([])),
        dcc.Graph(id='dotplot'),
        dcc.Store(id='dotplot-data', data=None)
    ])

    return dash_app, create_gene_plot, plot_dotplot