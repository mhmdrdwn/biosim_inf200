# -*- coding: utf-8 -*-

"""
Test set for landscapes class functionality and attributes.

This set of tests checks the landscapes classes methods perform as expected as per
the provided modeling.

"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

import pytest
import pandas
import glob
import os
import os.path

from biosim.simulation import BioSim
from biosim.landscapes import Landscapes
from biosim.landscapes import Desert, Ocean, Mountain, Savannah, Jungle
from biosim.fauna import Herbivore, Carnivore
from biosim.map import Map
import numpy as np


class TestMap:
    def test_string_to_np_array(self):
        map_str = """  OOOOOOOOOOOOOOOOOOOOO
                       OOOOOOOOSMMMMJJJJJJJO
                       OOOOOOOOOOOOOOOOOOOOO"""
        h1 = Herbivore()
        h1.fitness = 10
        h2 = Herbivore()
        h2.fitness = 20
        c1 = Carnivore()
        c1.fitness = 10
        c2 = Carnivore()
        c2.fitness = 20
        animals = {'Carnivore': [c1, c2], 'Herbivore': [h1, h2]}
        m = Map(map_str, animals)
        assert m.string_to_np_array()[0][0] == 'O'
        assert m.string_to_np_array()[1][10] == 'M'
        assert m.string_to_np_array()[2][20] == 'O'

# def test_migrate(self):





