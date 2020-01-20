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
from biosim.visualisation import Visualisation

# update these variables to point to your ffmpeg and convert binaries
_FFMPEG_BINARY = 'ffmpeg'
_CONVERT_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('../results', '')
_DEFAULT_GRAPHICS_NAME = 'biosim'
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
        self._island_map = island_map
        self._map = Map(island_map)
        self._vis = None
        self.add_population(ini_pop)

        if ymax_animals is None:
            self.ymax_animals = 16000 #adjust this automatically
        else:
            self.ymax_animals = ymax_animals

        if cmax_animals is None:
            self._cmax_animals = {'Herbivore': 10, 'Carnivore': 10}
        else:
            self._cmax_animals = cmax_animals

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

        self._year = 0
        self._final_year = None

        # the following will be initialized by _setup_graphics
        self._fig = None
        #self._img_axis = None

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

    def simulate(self, num_years, vis_years=None, img_years=None):
        """
        Run simulation while visualizing the result.
        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)
        Image files will be numbered consecutively.
        """
        if img_years is None:
            img_years = vis_years

        self._final_year = self._year + num_years
        self._setup_graphics()

        while self._year < self._final_year:

            if self._year % vis_years == 0:
                self._update_graphics()

            if self._year % img_years == 0:
                self._save_graphics()

            self._map.life_cycle()
            self._year += 1

    def _setup_graphics(self):
        """Creates subplots."""
        map_dims = self._map.cells_dims

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure()
            self._vis = Visualisation(self._island_map, self._fig, map_dims)

        self._vis.visualise_map()
        self._vis.animal_graphs(self._final_year, self.ymax_animals)

        # population distribution graphs
        self._vis.animal_dist_graphs()

    def _update_graphics(self):
        """Updates graphics with current data."""
        df = self.animal_distribution
        rows, cols = self._map.cells_dims
        dist_matrix_carnivore = np.array(df[['carnivore']]).reshape(rows, cols)
        dist_matrix_herbivore = np.array(df[['herbivore']]).reshape(rows, cols)
        self._update_animals_graph()
        self._vis.update_herbivore_dist(dist_matrix_herbivore,
                                        self._cmax_animals['Herbivore'])
        self._vis.update_carnivore_dist(dist_matrix_carnivore,
                                        self._cmax_animals['Carnivore'])
        plt.pause(1e-6)
        self._fig.suptitle('Year: '+str(self.year), x=0.1)

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

    def _update_animals_graph(self):
        herb_count, carn_count = list(self.num_animals_per_species.values())
        self._vis.update_graphs(self._year, herb_count, carn_count)

    @property
    def year(self):
        """Last year simulated."""
        return self._year

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
                count_df.append({'i': i, 'j': j,
                                 'carnivore': animals_count['Carnivore'],
                                 'herbivore': animals_count['Herbivore']})
        return pd.DataFrame(count_df)
