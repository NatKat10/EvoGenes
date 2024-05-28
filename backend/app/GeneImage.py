import json
import matplotlib.pyplot as plt
import mpld3
import numpy as np 

import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)

from yop_reader import process_sequences


"""
MIT License
Copyright (c) [2016] [Parashar Dhapola]
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__author__ = "Parashar Dhapola"
__email__ = "parashar.dhapola@gmail.com"


class GeneImage(object):
    def __init__(self, exon_intervals, marker_pos=[], marker_heights=[], marker_colors=[],
                 marker_size=100, marker_weight=1.5, exon_color="black", intron_color="grey",
                 intron_weight=2, intron_style='-', bar_color='cornflowerblue', bg_color="white"):
        self.exonIntervals = exon_intervals
        self.markerPositions = marker_pos
        self.markerHeights = marker_heights
        self.markerColors = marker_colors
        self.markerSize = marker_size
        self.MarkerWeight = marker_weight
        self.exonColor = exon_color
        self.intronColor = intron_color
        self.intronWeight = intron_weight
        self.intronStyle = intron_style
        self.barColor = bar_color
        self.bgColor = bg_color
        self.markerDefaultColor = 'grey'
        self.numExons = len(self.exonIntervals)
        self.totalSpan = self.exonIntervals[-1][1] - self.exonIntervals[0][0]
        self.minExonLen = self.totalSpan * 0.005
        self.ylims = {'exon_max': 1, 'exon_min': -1.5}
        self.figure, self.canvas = plt.subplots(figsize=(7, 1))
        self.canvas.set_facecolor(self.bgColor)

        self._draw()

    # def _set_limits(self):
    #     self.ylims['intron_max'] = self.ylims['exon_max'] * 0.9
    #     self.ylims['intron_min'] = (self.ylims['exon_max'] + self.ylims['exon_min']) / 2.0
    #     self.ylims['bar_min'] = self.ylims['exon_max'] + 0.2
    #     self.ylims['bar_max'] = self.ylims['bar_min'] + (self.ylims['exon_max'] - self.ylims['exon_min']) / 5.0

    def _set_limits(self):
        self.ylims['exon_max'] = 1
        self.ylims['exon_min'] = -1
        self.ylims['intron_max'] = 0.9
        self.ylims['intron_min'] = -0.1
        self.ylims['bar_min'] = 1.2
        self.ylims['bar_max'] = 1.4

    def _transform_spans(self):
        span_lens = [x[1] - x[0] for x in self.exonIntervals]
        max_len = float(max(span_lens))
        transformed_intervals = []
        if max_len < self.minExonLen:
            span_ratios = [x / max_len for x in span_lens]
            expansion_factor = self.totalSpan * 1e-11
            for i in range(1, 10):
                ef = (2 ** i) * expansion_factor
                if max_len + ef > self.minExonLen:
                    expansion_factor = ef
                    break
            for i, j in zip(self.exonIntervals, span_ratios):
                mid = (i[0] + i[1]) / 2
                f = (expansion_factor * j) / 2
                if mid + f - mid - f > self.minExonLen:
                    transformed_intervals.append([mid - f, mid + f])
                else:
                    transformed_intervals.append([mid - (self.minExonLen / 2), mid + (self.minExonLen / 2)])
        else:
            for i in range(self.numExons):
                if span_lens[i] < self.minExonLen:
                    mid = (self.exonIntervals[i][0] + self.exonIntervals[i][0]) / 2
                    transformed_intervals.append([mid - (self.minExonLen / 2), mid + (self.minExonLen / 2)])
                else:
                    transformed_intervals.append(self.exonIntervals[i])
        self.exonIntervals = transformed_intervals[:]


    def _draw_exon(self, span):
        self.canvas.fill_between(span, self.ylims['exon_min'], self.ylims['exon_max'],
                                edgecolor=self.bgColor, facecolor=self.exonColor, alpha=0.6)
        return True

    def _draw_intron(self, span):
        mid = (span[0] + span[1]) / 2.0
        self.canvas.plot([span[0], mid], [self.ylims['intron_min'], self.ylims['intron_max']],
                        c=self.intronColor, lw=self.intronWeight, ls=self.intronStyle, alpha=0.6)
        self.canvas.plot([mid, span[1]], [self.ylims['intron_max'], self.ylims['intron_min']],
                        c=self.intronColor, lw=self.intronWeight, ls=self.intronStyle, alpha=0.6)
        return True

    def _draw_markers(self):
        if self.markerHeights == []:
            self.markerHeights = [self.ylims['exon_max'] - self.ylims['exon_min'] for x in self.markerPositions]
        if self.markerColors == []:
            self.markerColors = [self.markerDefaultColor for x in self.markerPositions]
        for p, h, c in zip(self.markerPositions, self.markerHeights, self.markerColors):
            # self.canvas.plot((p, p), (self.ylims['bar_max'], self.ylims['bar_max'] + h),
            #                  linestyle='-', color='black', linewidth=self.MarkerWeight, alpha=0.7)
            # self.canvas.scatter(p, self.ylims['bar_max'] + h + 0.25, s=self.markerSize, marker='o', c=c,
            #                     edgecolor=c, alpha=1)
            self.canvas.scatter(p, self.ylims['bar_max'] + h + 1,  c=c,
                                 alpha=1)


    def _clean_axes(self):
        self.canvas.set_yticks([], [])
        self.canvas.get_xaxis().tick_bottom()  # Set the x-axis ticks to be at the bottom
        self.canvas.tick_params(axis='x', direction='out')
        self.canvas.set_xticks([])
        for o in ["top", "left", "right"]:  # Remove the top and left spines
            self.canvas.spines[o].set_visible(False)

        # Set the x-axis limits based on the exon intervals
        min_pos = self.exonIntervals[0][0]
        max_pos = self.exonIntervals[-1][1]
        x_range = max_pos - min_pos
        adjusted_min_pos = min_pos - 0.1 * x_range  # Adjust the x-axis limits to match yop_reader.py
        adjusted_max_pos = max_pos + 0.1 * x_range

        self.canvas.set_xlim(adjusted_min_pos, adjusted_max_pos)

        # Draw minor ticks and labels
        self._draw_minor_ticks_and_labels(adjusted_min_pos, adjusted_max_pos)

    def _draw_minor_ticks_and_labels(self, x_min, x_max):
        # Set the number of minor ticks and their positions
        num_minor_ticks = 10  # Adjust this value as needed
        minor_tick_positions = np.linspace(x_min, x_max, num_minor_ticks)

        # Draw minor ticks
        for pos in minor_tick_positions:
            self.canvas.axvline(pos, alpha=0, c='black', ls='--', clip_on=False)

        # Set x-axis tick locations and labels
        self.canvas.set_xticks(minor_tick_positions)
        minor_tick_labels = [int(pos) for pos in minor_tick_positions]
        self.canvas.set_xticklabels(minor_tick_labels, fontsize=8)

        # Ensure x-axis tick labels are visible
        plt.subplots_adjust(bottom=0.2)  # Adjust the bottom margin

        # Remove y-axis tick labels
        self.canvas.set_yticks([])


    def _draw(self):
        self._set_limits()
        self._transform_spans()
        for i in range(self.numExons):
            if i > 0:
                self._draw_intron([self.exonIntervals[i - 1][1], self.exonIntervals[i][0]])
            self._draw_exon(self.exonIntervals[i])
        self._clean_axes()

    def show(self):
        plt.show()

    def save_plot(self, output_path='gene_image.png'):
        """
        Save the gene image plot to a file.
        :param output_path: Path to save the plot image.
        """
        plt.savefig(output_path)

    def show_mpld3(self):
        mpld3.show()

    def get_figure_html(self):
        # Create the Matplotlib figure
        self.figure, self.canvas = plt.subplots(figsize=(7, 1))
        self.canvas.set_facecolor(self.bgColor)

        # Call the internal functions to draw the plot
        self._set_limits()
        self._transform_spans()
        self._draw()

        # Convert the figure to HTML using mpld3
        figure_html = mpld3.fig_to_html(self.figure, d3_url=None, mpld3_url=None, no_extras=True)

        return figure_html

