# -*- coding: utf-8 -*-

"""
Test set for landscapes class functionality and attributes.

This set of tests checks the landscapes classes methods perform as expected as
per the provided modeling.

"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

import pytest
from biosim.landscapes import Desert, Ocean, Mountain, Savannah, Jungle
from biosim.fauna import Herbivore, Carnivore
from biosim.map import Map
from scipy import stats
import mock
from mock import patch
from random import seed
import numpy as np


class TestGaussian:
    @pytest.fixture
    def generate_animal_data(self):
        """
        Generates population of animals and an array of their initial weight.

        Returns
        -------
        birth_weight_list: list
            list of animals' initial weight
        """
        birth_weight_list = []
        for _ in range(20):
            carn = Carnivore()
            carn.set_default_weight()
            birth_weight_list.append(carn.weight)
        for _ in range(20):
            h = Herbivore()
            h.set_default_weight()
            z = h.weight
            birth_weight_list.append(z)
        return birth_weight_list

    def test_birth_weight_dist(self, generate_animal_data):
        """
        Returns whether the null hypothesis is rejected or not by comparing if
        P_value is less than alpha = 1% or not. Null hypothesis is
        "birth_weight_list comes from a normal distribution"

        Parameters
        ----------
        generate_animal_data: list
            list of animals' birth weight
        """
        birth_weight_list = generate_animal_data
        k2, p_value = stats.normaltest(birth_weight_list)
        alpha = 0.01
        if p_value < alpha:
            print("The null hypothesis can be rejected")
        else:
            print("The null hypothesis cannot be rejected")


class TestProbability:
    """
    Tests the method die_animal as of using mock: Replacing random number
    generator with fixed value.
    """
    def test_die(mocker):
        herb_1 = Herbivore(6, 0)
        herb_2 = Herbivore()
        carn_1 = Carnivore(1,5)
        carn_2 = Carnivore()
        params = {'f_max': 10.0}
        j=Jungle(params)
        j.add_animal(carn_1)
        j.add_animal(carn_2)
        j.add_animal(herb_1)
        j.add_animal(herb_2)
        herb_1.calculate_fitness()
        assert herb_1.death_prob
        herb_2.calculate_fitness()
        carn_1.calculate_fitness()
        carn_2.calculate_fitness()
        mock.Mock()
        mock.patch('numpy.random.random', return_value=0.00049292282)
        j.die_animals()
        h_count = len(j.in_cell_fauna['Herbivore'])
        c_count = len(j.in_cell_fauna['Carnivore'])
        fauna_count = h_count + c_count
        print(fauna_count)
        assert fauna_count == 2

