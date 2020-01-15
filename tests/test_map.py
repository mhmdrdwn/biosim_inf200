# -*- coding: utf-8 -*-

"""
Test set for landscapes class functionality and attributes.

This set of tests checks the landscapes classes methods perform as expected as per
the provided modeling.

"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from random import seed

import pytest

from biosim.landscapes import Desert, Ocean, Mountain, Savannah, Jungle
from biosim.fauna import Herbivore, Carnivore
from biosim.map import Map
import numpy as np


class TestMap:
    @pytest.fixture
    def gen_animal_data(self):
        seed(1)
        h1 = Herbivore()
        h2 = Herbivore()
        seed(1)
        c1 = Carnivore()
        c2 = Carnivore()
        return c1, c2, h1, h2

    @pytest.fixture
    def gen_landscape_data(self, gen_animal_data):
        landscape_params = {'f_max': 10.0}
        c1, c2, h1, h2 = gen_animal_data
        animals = {'Herbivore': [h1, h2], 'Carnivore': [c1, c2]}
        landscapes_dict = {'s': Savannah(animals, landscape_params),
                           'o': Ocean(),
                           'd': Desert(animals),
                           'm': Mountain(),
                           'j': Jungle(animals, landscape_params)}
        return landscapes_dict

    @pytest.fixture
    def gen_map_data(self, gen_landscape_data):
        pass

    def test_string_to_np_array(self):
        map_str = """  OOOOOOOOOOOOOOOOOOOOO
                       OOOOOOOOSMMMMJJJJJJJO
                       OOOOOOOOOOOOOOOOOOOOO"""
        m = Map(map_str)
        assert m.string_to_np_array()[0][0] == 'O'
        assert m.string_to_np_array()[1][10] == 'M'
        assert m.string_to_np_array()[2][20] == 'O'
        assert type(m.string_to_np_array()).__name__ == 'ndarray'

    def test_create_map(self):
        map_str = """  OSOOOOOOOOOOOOOOOOOOO
                       OOOOOOOOSMMMMJJJJJJJO
                       OOOOOOOOOOOOOOOOOOOOO"""
        m = Map(map_str)
        assert isinstance(m.create_map()[0][0], Ocean)
        assert isinstance(m.create_map()[1][10], Mountain)
        assert isinstance(m.create_map()[2][20], Ocean)
        assert isinstance(m.create_map()[0][1], Savannah)

# def test_migrate(self):





