# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

import os
import textwrap

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import subprocess

from biosim.fauna import Herbivore, Carnivore
from biosim.landscapes import Ocean, Savannah, Desert, Jungle, Mountain
from biosim.map import Map

# update these variables to point to your ffmpeg and convert binaries
_FFMPEG_BINARY = 'ffmpeg'
_CONVERT_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('..', 'data')
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_MOVIE_FORMAT = 'mp4'  # alternatives: mp4, gif


class BioSim:
    def __init__(
            self,
            island_map,
            ini_pop,
            seed,
            ymax_animals=None,
            cmax_animals=None,
            img_base=None,
            img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'
        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}
        If img_base is None, no figures are written to file.
        Filenames are formed as
            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)
        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        np.random.seed(seed)
        self._map = Map(island_map)
        self.add_population(ini_pop)
        if ymax_animals is None:
            self.ymax_animals = None
        else:
            self.ymax_animals = ymax_animals

        if cmax_animals is None:
            self.cmax_animals = None
            # need to add the color pallete here
        else:
            self.cmax_animals = cmax_animals

        if img_base is None:
            self._img_base = _DEFAULT_GRAPHICS_DIR + _DEFAULT_GRAPHICS_NAME
        else:
            self._img_base = img_base
        self._img_ctr = 0
        self._img_fmt = img_fmt

        self.landscapes = {'O': Ocean,
                           'S': Savannah,
                           'M': Mountain,
                           'J': Jungle,
                           'D': Desert}
        self.landscapes_with_changable_parameters = [Savannah, Jungle]
        self.animal_species = ['Carnivore', 'Herbivore']

        # color pallette for landscapes/cells
        self._landscape_colors = {'S': mcolors.to_rgb('springgreen'),
                                  'D': mcolors.to_rgb('navajowhite'),
                                  'O': mcolors.to_rgb('blue'),
                                  'M': mcolors.to_rgb('silver'),
                                  'J': mcolors.to_rgb('forestgreen')}

        self._cells_colors = [[self._landscape_colors[letter] for letter in
                               line] for line in geogr.splitlines()]

        self._step = 0
        self._final_step = None

        # the following will be initialized by _setup_graphics
        self._fig = None
        self._map_ax = None
        self._img_axis = None
        self._mean_ax = None
        self._herbivore_line = None
        self._carnivore_line = None
        self._herbivore_dist = None
        self._carnivore_dist = None
        self._year = 0

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.
        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species in self.animal_species:
            species_class = eval(species)
            species_class.set_given_parameters(params)
        else:
            raise TypeError(species + ' parameters can\'t be assigned, '
                                      'there is no such data type')

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.
        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape in self.landscapes:
            landscape_class = self.landscapes[landscape]
            if landscape_class in \
                    self.landscapes_with_changable_parameters:
                landscape_class.set_given_parameters(params)
            else:
                raise ValueError(landscape + ' parameters is not valid')

        else:
            raise TypeError(landscape + ' parameters can\'t be assigned, '
                                        'there is no such data type')

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.
        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)
        Image files will be numbered consecutively.
        """
        if img_years is None:
            img_years = vis_years

        self._final_step = self._step + num_years
        self._setup_graphics()

        while self._step < self._final_step:

            if self._step % vis_years == 0:
                self._update_graphics()

            if self._step % img_years == 0:
                self._save_graphics()

            self._map.update()
            self._step += 1

    def _build_map(self):
        y, x = self._map.cells_dims
        self._map_ax = self._fig.add_subplot(2, 2, 1)
        self._map_ax.imshow(self._cells_colors)
        self._map_ax.set_xticks(range(0, x, 5))
        self._map_ax.set_xticklabels(range(1, 1 + x, 5))
        self._map_ax.set_yticks(range(0, y, 5))
        self._map_ax.set_yticklabels(range(1, 1 + y, 5))
        self._map_ax.set_title('Island')
        plt.show()

    def _build_carn_sim(self):
        if self._carnivore_line is None:
            carnivore_plot = self._mean_ax.plot(np.arange(0, self._final_step),
                                                np.full(self._final_step,
                                                        np.nan))
            self._carnivore_line = carnivore_plot[0]
        else:
            xdata, ydata = self._carnivore_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self._final_step)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._carnivore_line.set_data(np.hstack((xdata, xnew)),
                                              np.hstack((ydata, ynew)))

    def _build_herb_sim(self):
        if self._herbivore_line is None:
            herbivore_plot = self._mean_ax.plot(np.arange(0, self._final_step),
                                                np.full(self._final_step,
                                                        np.nan))
            self._herb_line = herbivore_plot[0]
        else:
            xdata, ydata = self._herbivore_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self._final_step)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._herbivore_line.set_data(np.hstack((xdata, xnew)),
                                              np.hstack((ydata, ynew)))
        plt.show()

    def _setup_graphics(self):
        """Creates subplots."""

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure()

        if self._map_ax is None:
            self._build_map()

        # Add right subplot for line graph of mean.
        if self._mean_ax is None:
            self._mean_ax = self._fig.add_subplot(2, 2, 2)
            self._mean_ax.set_ylim(0, 10000)

        # needs updating on subsequent calls to simulate()
        #self._mean_ax.set_xlim(0, self._final_step + 1)
        self._build_herb_sim()
        self._build_carn_sim()

        # population distribution graphs
        if self._herbivore_dist is None:
            self._herbivore_dist = self._fig.add_subplot(2, 2, 3)
            #what to add here
        if self._carnivore_dist is None:
            self._carnivore_dist = self._fig.add_subplot(2, 2, 4)
            #what to add here

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

    def _update_mean_graph(self, mean):
        ydata = self._mean_line.get_ydata()
        ydata[self._step] = mean
        self._mean_line.set_ydata(ydata)

    def _update_graphics(self):
        """Updates graphics with current data."""
        self._update_system_map(self.animal_distribution)
        # self._update_mean_graph(self._map.mean_value())
        plt.pause(1e-6)

    def _save_graphics(self):
        """Saves graphics to file if file name given."""

        if self._img_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1

    def add_population(self, population):
        """
        Add a population to the island
        :param population: List of dictionaries specifying population
        """
        self._map.add_animals(population)

    def make_movie(self, movie_fmt=_DEFAULT_MOVIE_FORMAT):
        """
        Creates MPEG4 movie from visualization images saved.
        .. :note:
            Requires ffmpeg
        The movie is stored as img_base + movie_fmt
        """

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i',
                                       '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_CONVERT_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError(
                    'ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    @property
    def year(self):
        """Last year simulated."""
        return self._step

    @property
    def num_animals(self):
        """Total number of animals on island."""
        total_num = 0
        for species in self.animal_species:
            total_num += self._map.total_num_animals_per_species(species)
        return total_num

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        num_per_species = {}
        for species in self.animal_species:
            num_per_species[species] = \
                self._map.total_num_animals_per_species(species)
        return num_per_species

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each
        cell on island."""
        count_df = []
        rows, cols = self._map.cells_dims
        for i in range(rows):
            for j in range(cols):
                cell = self._map.cells[i, j]
                animals_count = cell.cell_fauna_count
                loc = i, j
                count_df.append({'Cell': loc, 'Num of Animals': animals_count})
        return pd.DataFrame(count_df)


if __name__ == '__main__':
    geogr = """\
               OOOOOOOOOOOOOOOOOOOOO
               OOOOOOOOSMMMMJJJJJJJO
               OSSSSSJJJJMMJJJJJJJOO
               OSSSSSSSSSMMJJJJJJOOO
               OSSSSSJJJJJJJJJJJJOOO
               OSSSSSJJJDDJJJSJJJOOO
               OSSJJJJJDDDJJJSSSSOOO
               OOSSSSJJJDDJJJSOOOOOO
               OSSSJJJJJDDJJJJJJJOOO
               OSSSSJJJJDDJJJJOOOOOO
               OOSSSSJJJJJJJJOOOOOOO
               OOOSSSSJJJJJJJOOOOOOO
               OOOOOOOOOOOOOOOOOOOOO"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]
    ini_carns = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(50)
            ],
        }
    ]
    ini_carns2 = [
        {
            "loc": (5, 5),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(50)
            ],
        }
    ]
    sim = BioSim(island_map=geogr, ini_pop=ini_herbs, seed=123456)
    sim.add_population(ini_carns)
    sim.add_population(ini_carns2)

    print(sim.num_animals_per_species)
    print(sim.num_animals)
    print(sim.animal_distribution)
    sim._setup_graphics()
    # print(len(sim._cells_colors[0]))
    # print(len(geogr.splitlines()))

    test = np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]])
    # print(test.shape)
