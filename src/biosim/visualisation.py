# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'


import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

class Visualisation:
    map_colors = {
        "O": mcolors.to_rgba("navy"),
        "J": mcolors.to_rgba("forestgreen"),
        "S": mcolors.to_rgba("springgreen"),
        "D": mcolors.to_rgba("navajowhite"),
        "M": mcolors.to_rgba("lightslategrey"),
    }
    map_labels = {
        "O": "Ocean",
        "J": "Jungle",
        "S": "Savannah",
        "D": "Desert",
        "M": "Mountain",
    }

    def __init__(self, map_layout, figure, map_dims):
        self._map_layout = map_layout
        self._fig = figure
        self._map_colors = Visualisation.map_colors
        self._map_dims = map_dims
        self._map_ax = None
        self._mean_ax = None
        self._herbivore_curve = None
        self._carnivore_curve = None
        self._herbivore_dist = None
        self._carnivore_dist = None

    def generate_map_array(self):
        """Transform the string that parametrises the map into an rgba image.
        """

        lines = self._map_layout.splitlines()
        if len(lines[-1]) == 0:
            lines = lines[:-1]

        num_cells = len(lines[0])
        map_array = []
        for line in lines:
            map_array.append([])
            if num_cells != len(line):
                raise ValueError(
                    "All lines in the map must have the same number of cells."
                )
            for letter in line:
                if letter not in self.map_colors:
                    raise ValueError(
                        f"'{letter}' is not a valid landscape type. "
                        f"Must be one of {set(self._map_colors.keys)}"
                    )
                map_array[-1].append(self.map_colors[letter])

        return map_array

    def visualise_map(self):
        """Create a map over the island
        """
        self._map_ax = self._fig.add_subplot(2, 2, 1)
        y, x = self._map_dims
        self._map_ax.imshow(self.generate_map_array())
        self._map_ax.set_xticks(range(0, x, 5))
        self._map_ax.set_xticklabels(range(0, x, 5))
        self._map_ax.set_yticks(range(0, y, 5))
        self._map_ax.set_yticklabels(range(0, y, 5))
        self._map_ax.set_title('Island')
        #self.add_map_legend()

    def add_map_legend(self):
        for i, (landscape, color) in enumerate(self.map_colors.items()):
            label = self.map_labels[landscape]
            self._legend_ax.add_patch(
                plt.Rectangle(
                    (0.0, i * 0.2),
                    width=0.1,
                    height=0.1,
                    edgecolor=None,
                    facecolor=color,
                )
            )
            self._legend_ax.text(
                x=0.2,
                y=0.05 + i * 0.2,
                s=self.map_labels[landscape],
                verticalalignment="center",
                weight="bold",
                size=18,
            )

        self._legend_ax.axis("off")
        self._legend_ax.set_ylim(0, i * 0.2 + 0.1)

    def _build_carn_sim_graph(self, final_step):
        if self._carnivore_curve is None:
            carnivore_plot = self._mean_ax.plot(np.arange(0, final_step),
                                                np.full(final_step,
                                                        np.nan))
            self._carnivore_curve = carnivore_plot[0]
        else:
            xdata, ydata = self._carnivore_curve.get_data()
            xnew = np.arange(xdata[-1] + 1, final_step)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._carnivore_curve.set_data(np.hstack((xdata, xnew)),
                                              np.hstack((ydata, ynew)))

    def _build_herb_sim_graph(self, final_step):
        if self._herbivore_curve is None:
            herbivore_plot = self._mean_ax.plot(np.arange(0, final_step),
                                                np.full(final_step,
                                                        np.nan))
            self._herbivore_curve = herbivore_plot[0]
        else:
            xdata, ydata = self._herbivore_curve.get_data()
            xnew = np.arange(xdata[-1] + 1, final_step)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._herbivore_curve.set_data(np.hstack((xdata, xnew)),
                                              np.hstack((ydata, ynew)))

    def animal_graphs(self, final_step):
        if self._mean_ax is None:
            self._mean_ax = self._fig.add_subplot(2, 2, 2)
            self._mean_ax.set_ylim(0, 100)
        self._mean_ax.set_xlim(0, final_step + 1)
        self._build_herb_sim_graph(final_step)
        self._build_carn_sim_graph(final_step)

    def animal_dist_graphs(self):
        # population distribution graphs
        if self._herbivore_dist is None:
            self._herbivore_dist = self._fig.add_subplot(2, 2, 3)

        if self._carnivore_dist is None:
            self._carnivore_dist = self._fig.add_subplot(2, 2, 4)
            # what to add here

    def update_herbivore_graph(self, distribution):
        y, x = self._map_dims
        self._herbivore_dist.imshow(distribution)
        self._herbivore_dist.set_xticks(range(0, x, 5))
        self._herbivore_dist.set_xticklabels(range(1, 1 + x, 5))
        self._herbivore_dist.set_yticks(range(0, y, 5))
        self._herbivore_dist.set_yticklabels(range(1, 1 + y, 5))
        self._herbivore_dist.set_title('Herbivore Distribution')

    def update_carnivore_graph(self, distribution):
        y, x = self._map_dims
        self._carnivore_dist.imshow(distribution)
        self._carnivore_dist.set_xticks(range(0, x, 5))
        self._carnivore_dist.set_xticklabels(range(1, 1 + x, 5))
        self._carnivore_dist.set_yticks(range(0, y, 5))
        self._carnivore_dist.set_yticklabels(range(1, 1 + y, 5))
        self._carnivore_dist.set_title('Carnivore Distribution')

    def _update_system_map(self, sys_map):
        """Update the 2D-view of the system."""

        if self._img_axis is not None:
            self._img_axis.set_data(sys_map)
        else:
            self._img_axis = self._map_ax.imshow(sys_map,
                                                 interpolation='nearest',
                                                 vmin=0, vmax=1)
            plt.colorbar(self._img_axis, ax=self._map_ax,
                         orientation='horizontal')