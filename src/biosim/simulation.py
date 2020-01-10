# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

import numpy as np
import pandas as pd
import itertools
from biosim.landscapes import *
#that's wrong

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
        self.island_map = island_map
        self.ini_pop = ini_pop
        np.random.seed(seed)
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
        for i in range(num_years):
            # update the last year
            self.last_year += vis_years
            '{}_{:05d}.{}'.format(self.img_base, i, self.img_fmt)

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        # loc = population[0]['loc']
        # for element in self.ini_pop:
        #    if element['loc'] == loc:
        #        for item in population[0]['pop']:
        #            element['pop'].append(item)
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

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""


# importing pandas as pd

# list of name, degree, score
nme = ["aparna", "pankaj", "sudhir", "Geeku"]
deg = ["MBA", "BCA", "M.Tech", "MBA"]
scr = [90, 40, 80, 98]

# dictionary of lists
dict = {'name': nme, 'degree': deg, 'score': scr}

df = pd.DataFrame(dict)

# saving the dataframe
df.to_csv('file1.csv')

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
