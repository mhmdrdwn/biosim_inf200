# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'


import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


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
        self._figure = figure
        self._map_ax = None
        self._map_colors = Visualisation.map_colors
        self._map_dims = map_dims

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
        self._map_ax = self._figure.add_subplot(2, 2, 1)
        y, x = self._map_dims
        self._map_ax.imshow(self.generate_map_array())
        self._map_ax.set_xticks(range(0, x, 5))
        self._map_ax.set_xticklabels(range(1, 1 + x, 5))
        self._map_ax.set_yticks(range(0, y, 5))
        self._map_ax.set_yticklabels(range(1, 1 + y, 5))
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