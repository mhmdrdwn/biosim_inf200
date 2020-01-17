# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
        self._map = Map(island_map, ini_pop)
        if ymax_animals is None:
            self.ymax_animals = len(ini_pop[0]['pop'])
        else:
            self.ymax_animals = ymax_animals
        if cmax_animals is None:
            self.cmax_animals = None
            # need to add the color pallete here
        else:
            self.cmax_animals = cmax_animals

        self.img_fmt = img_fmt

        self.landscapes = {'O': Ocean,
                           'S': Savannah,
                           'M': Mountain,
                           'J': Jungle,
                           'D': Desert}
        self.landscapes_with_changable_parameters = [Savannah, Jungle]
        self.animal_species = ['Carnivore', 'Herbivore']

        self._step = 0
        self._final_step = None

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

            self._system.update()
            self._step += 1

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
                                       '-i', '{}_%05d.png'.format(self._img_base),
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
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)



    @property
    def year(self):
        """Last year simulated."""

    @property
    def num_animals(self):
        """Total number of animals on island."""

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""


if __name__ == '__main__':
    import textwrap

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
    c1 = Carnivore()
    h1 = Herbivore()
    c2 = Carnivore()
    h2 = Herbivore()
    animals = {'Herbivore': [h1, h2], 'Carnivore': [c1, c2]}
    s = Savannah(animals)
    print(s.parameters)
    # c1 = Carnivore()
    # h1 = Herbivore()
    # print('c1' + str(c1.parameters))
    # print('h1' + str(h1.parameters))
    # biosim.set_animal_parameters("Carnivore", {"zeta": 7777777, "xi": 1.8})
    biosim.set_landscape_parameters("S", {"f_max": 777})
    print(s.parameters)
    biosim.add_population(ini_carns)
    print(Map.all_fauna)
    biosim.add_population(ini_carns)
    print(Map.all_fauna)
    # c2 = Carnivore()
    # h2 = Herbivore()
    # print('c2' + str(c2.parameters))
    # print('h2' + str(h2.parameters))
