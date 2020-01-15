# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

import numpy as np
import pandas as pd
import matplotlib.colors as color
import matplotlib.pyplot as plt
import subprocess
import os
from biosim.map import *
import textwrap


# update these variables to point to  ffmpeg and convert binaries
_FFMPEG_BINARY = 'ffmpeg'
_CONVERT_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_IMG_BASE = os.path.join('..', 'data')
_DEFAULT_GRAPHICS_NAME = 'bio'
_DEFAULT_MOVIE_FORMAT = 'mp4'   # alternatives: mp4, gif


class BioSim:
    def __init__(
            self,
            island_map,
            ini_pop,
            seed,
            ymax_animals=None,
            cmax_animals=None,
            img_base=None,
            img_fmt='png'
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
        fauna_objects = {}
        self._system = Map(island_map, fauna_objects)

        self.island_map = island_map
        self.ini_pop = ini_pop
        np.random.seed(seed)
        self.cell_color = {'O': color.to_rgb('blue'),
                         'M': color.to_rgb('brown'),
                         'J': color.to_rgb('darkgreen'),
                         'S': color.to_rgb('green'),
                         'D': color.to_rgb('cream')}

        self.ymax_animals = ymax_animals
        if self.ymax_animals is None:
            self.ymax_animals = len(ini_pop[0]['pop'])
        self.cmax_animals = cmax_animals
        if cmax_animals is None:
            ini_species = ini_pop[0]['pop'][0]['species']
            self.cmax_animals = {ini_species: len(ini_pop[0]['pop'])}
            # need to ask about that
        self.img_base = img_base
        if img_base is None:
            self.img_base = None
        self.img_fmt = img_fmt
        self.fauna_parameters = {'Herbivore': {}, 'Carnivore': {}}
        self.landscape_parameters = {'O': {}, 'J': {}, 'S': {}, 'D': {},
                                     'M': {}}
        self.last_year = 0
        self.sorted_ = []


        self._year = 0
        self._final_year = None
        self._img_ctr = 0

        # the following will be initialized by _setup_graphics
        self._fig = None
        self._map_ax = None
        self._img_axis = None
        self._mean_ax = None
        self._mean_line = None

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        for param in params:
            self.fauna_parameters[species][param] = params[param]

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        for param in params:
            self.fauna_parameters[landscape][param] = params[param]

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

        self._final_year = self._year + num_years
        self._setup_graphics()

        while self._year < self._final_year:
            if self._year % vis_years == 0:
                self._update_graphics()

            if self._year % img_years == 0:
                self._save_graphics()

            for i in range(num_years):
                # update the last year
                self.last_year += vis_years
                '{}_{:05d}.{}'.format(self.img_base, i, self.img_fmt)

            self._year += 1



    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.ini_pop.append(population[0])




    def sort(self):
        def key_func(x):
            return x['loc']

        self.ini_pop = sorted(self.ini_pop, key=key_func)

    @property
    def year(self):
        """Last year simulated."""
        return self.last_year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        count = 0
        for element in self.ini_pop:
            count += len(element['pop'])
        return count

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        num_animals_dict = {'Herbivore': 0, 'Carnivore': 0}
        for element in self.ini_pop:
            key = element['pop'][0]['species']
            num_animals_dict[key] += len(element['pop'])
        return num_animals_dict

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each
        cell on island."""
        cell_list = []
        num_animals_list = []
        i = 0
        for element in self.ini_pop:
            if element['loc'] not in cell_list:
                cell_list.append(element['loc'])
                num_animals_list.append(len(element['pop']))
                i += 1
            else:
                num_animals_list[i-1] += len(element['pop'])
        df_dict = {'Cell': cell_list, 'Num of Animals': num_animals_list}
        print(len(cell_list))
        return pd.DataFrame(df_dict)


    def make_movie(self, movie_fmt=_DEFAULT_MOVIE_FORMAT):
        """
        Creates MPEG4 movie from visualization images saved.
        .. :note:
            Requires ffmpeg
        The movie is stored as img_base + movie_fmt
        """

        if self.img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self.img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self.img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_CONVERT_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self.img_base),
                                       '{}.{}'.format(self.img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)


    def _setup_graphics(self):
        """Creates subplots."""

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure()

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(1, 2, 1)
            self._img_axis = None

        # Add right subplot for line graph of mean.
        if self._mean_ax is None:
            self._mean_ax = self._fig.add_subplot(1, 2, 2)
            self._mean_ax.set_ylim(0, 0.02)

        # needs updating on subsequent calls to simulate()
        self._mean_ax.set_xlim(0, self._final_year + 1)

        if self._mean_line is None:
            mean_plot = self._mean_ax.plot(np.arange(0, self._final_year),
                                           np.full(self._final_year, np.nan))
            self._mean_line = mean_plot[0]
        else:
            xdata, ydata = self._mean_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self._final_year)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._mean_line.set_data(np.hstack((xdata, xnew)),
                                         np.hstack((ydata, ynew)))


    def _update_system_map(self, sys_map):

        '''Update the 2D-view of the system.
        distribution per cell is represented as a
        2D heat map.
        '''

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
        ydata[self._year] = mean
        self._mean_line.set_ydata(ydata)


    def _update_graphics(self):
        """Updates graphics with current data."""

        self._update_system_map(self._system.get_status())
        self._update_mean_graph(self._system.mean_value())
        plt.pause(1e-6)

        self._fig.suptitle('Year: {}'.format(self._year + 1), x=0.105)  # x value should be change

    def _save_graphics(self):
        """Saves graphics to file if file name given."""

        if self.img_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self.img_base,
                                                     num=self._img_ctr,
                                                     type=self.img_fmt))
        self._img_ctr += 1




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
            for _ in range(3)
        ],
    }
]
ini_carns = [
    {
        "loc": (20, 20),
        "pop": [
            {"species": "Carnivore", "age": 5, "weight": 20}
            for _ in range(5)
        ],
    }
]
ini_carns2 = [
    {
        "loc": (10, 10),
        "pop": [
            {"species": "Carnivore", "age": 5, "weight": 20}
            for _ in range(4)
        ],
    }
]
ini_carns3 = [
    {
        "loc": (30, 30),
        "pop": [
            {"species": "Carnivore", "age": 5, "weight": 20}
            for _ in range(5)
        ],
    }
]
ini_carns4 = [
    {
        "loc": (40, 40),
        "pop": [
            {"species": "Carnivore", "age": 5, "weight": 20}
            for _ in range(5)
        ],
    }
]
biosim = BioSim(island_map=geogr, ini_pop=ini_herbs, seed=123456)
biosim.set_animal_parameters("Herbivore", {"zeta": 3.2, "xi": 1.8})
# print(biosim.cmax_animals)
# print(biosim.fauna_parameters)
# print(biosim.ymax_animals)
biosim.add_population(ini_carns)
biosim.add_population(ini_carns2)
biosim.add_population(ini_carns2)
biosim.add_population(ini_carns)
biosim.add_population(ini_carns3)
biosim.add_population(ini_carns4)
biosim.sort()
print(biosim.ini_pop)
print(type(biosim.ini_pop))
print(biosim.ini_pop)
print(biosim.num_animals_per_species)
print(biosim.num_animals)
# print(biosim.ini_pop[0])
# print(biosim.ini_pop[1])
print(biosim.animal_distribution)
