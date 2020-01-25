# -*- coding: utf-8 -*-

"""
Visualisation class handles the setup of all graph and heatmap to
show the simulated data each year.
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


class Visualisation:
    """
    Visualises the BioSim simulation by making graphs and movie.
    """
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
        """
        The constructor for the Visualisation class.

        Parameters
        ----------
        map_layout: str
        figure: matplotlib figure
        map_dims: int
        """
        self._map_layout = map_layout
        self._fig = figure
        self._map_colors = Visualisation.map_colors
        self._map_dims = map_dims
        self._mean_ax = None
        self._map_graph = None
        self._herbivore_curve = None
        self._carnivore_curve = None
        self._herbivore_dist = None
        self._carnivore_dist = None
        self._herbivore_img_axis = None
        self._carnivore_img_axis = None

    def generate_map_array(self):
        """
        Transform the string that parametrises the map into an rgba image.

        Returns
        -------
        map_array: array
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
                        f"Must be one of {set(self._map_colors.keys())}"
                    )
                map_array[-1].append(self.map_colors[letter])

        return map_array

    def visualise_map(self):
        """
        Creates a map over the island.
        """
        if self._map_graph is None:
            self._map_graph = self._fig.add_subplot(2, 2, 1)
            y, x = self._map_dims
            self._map_graph.imshow(self.generate_map_array())
            self._map_graph.set_xticks(range(0, x, 5))
            self._map_graph.set_xticklabels(range(1, x + 1, 5))
            self._map_graph.set_yticks(range(0, y, 5))
            self._map_graph.set_yticklabels(range(1, y + 1, 5))
            self._map_graph.set_title('Island')

    def _build_carn_sim_curve(self, final_year):
        """
        Makes 2D simulation curve for carnivores.

        Parameters
        ----------
        final_year: int
        """
        if self._carnivore_curve is None:
            plot = self._mean_ax.plot(np.arange(0, final_year),
                                      np.full(final_year, np.nan))
            self._carnivore_curve = plot[0]
        else:
            xdata, ydata = self._carnivore_curve.get_data()
            xnew = np.arange(xdata[-1] + 1, final_year)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                x_stack = np.hstack((xdata, xnew))
                y_stack = np.hstack((ydata, ynew))
                self._carnivore_curve.set_data(x_stack, y_stack)

    def _build_herb_sim_curve(self, final_year):
        """
        Makes 2D simulation curve for herbivores.

        Parameters
        ----------
        final_year: int
        """
        if self._herbivore_curve is None:
            plot = self._mean_ax.plot(np.arange(0, final_year),
                                      np.full(final_year, np.nan))
            self._herbivore_curve = plot[0]
        else:
            xdata, ydata = self._herbivore_curve.get_data()
            xnew = np.arange(xdata[-1] + 1, final_year)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                x_stack = np.hstack((xdata, xnew))
                y_stack = np.hstack((ydata, ynew))
                self._herbivore_curve.set_data((x_stack, y_stack))

    def update_graphs(self, year, herb_count, carn_count):
        """
        Updates the graph curves for both herbivores and carnivores.

        Parameters
        ----------
        year: int
        herb_count: int
        carn_count: int
        """
        herb_ydata = self._herbivore_curve.get_ydata()
        herb_ydata[year] = herb_count
        self._herbivore_curve.set_ydata(herb_ydata)

        carn_ydata = self._carnivore_curve.get_ydata()
        carn_ydata[year] = carn_count
        self._carnivore_curve.set_ydata(carn_ydata)
        plt.pause(1e-4)

    def animal_graphs(self, final_year, y_lim):
        """
        Settings up the lines.

        Parameters
        ----------
        final_year: int
        y_lim: int
        """
        if self._mean_ax is None:
            self._mean_ax = self._fig.add_subplot(2, 2, 2)
            self._mean_ax.set_ylim(0, y_lim)
        self._mean_ax.set_xlim(0, final_year + 1)
        self._build_herb_sim_curve(final_year)
        self._build_carn_sim_curve(final_year)
        self._mean_ax.set_title('Animals population')

    def animal_dist_graphs(self):
        """
        Plots animal distribution
        """
        if self._herbivore_dist is None:
            self._herbivore_dist = self._fig.add_subplot(2, 2, 3)
            self._herbivore_img_axis = None

        if self._carnivore_dist is None:
            self._carnivore_dist = self._fig.add_subplot(2, 2, 4)
            self._carnivore_img_axis = None

    def update_herbivore_dist(self, distribution):
        """
        Updates herbivores distribution.

        Parameters
        ----------
        distribution: data frame
        """
        v_max = distribution.max()
        v_min = distribution.min()
        if self._herbivore_img_axis is not None:
            self._herbivore_img_axis.set_data(distribution)
        else:
            y, x = self._map_dims
            self._herbivore_dist.imshow(distribution,
                                        interpolation='nearest',
                                        vmin=v_min, vmax=v_max)
            self._herbivore_dist.set_xticks(range(0, x, 5))
            self._herbivore_dist.set_xticklabels(range(1, 1 + x, 5))
            self._herbivore_dist.set_yticks(range(0, y, 5))
            self._herbivore_dist.set_yticklabels(range(1, 1 + y, 5))
            self._herbivore_dist.set_title('Herbivore Distribution')

    def update_carnivore_dist(self, distribution):
        """
        Updates carnivores distribution.

        Parameters
        ----------
        distribution: str
        """
        v_max = distribution.max()
        v_min = distribution.min()
        if self._carnivore_img_axis is not None:
            self._carnivore_img_axis.set_data(distribution)
        else:
            y, x = self._map_dims
            self._carnivore_dist.imshow(distribution,
                                        interpolation='nearest',
                                        vmin=v_min, vmax=v_max)
            self._carnivore_dist.set_xticks(range(0, x, 5))
            self._carnivore_dist.set_xticklabels(range(1, 1 + x, 5))
            self._carnivore_dist.set_yticks(range(0, y, 5))
            self._carnivore_dist.set_yticklabels(range(1, 1 + y, 5))
            self._carnivore_dist.set_title('Carnivore Distribution')

