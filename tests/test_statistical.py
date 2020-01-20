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
from scipy import stats
import mock
from mock import patch


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
            c = Carnivore()
            c.set_default_attribute('weight')
            x = c.weight
            birth_weight_list.append(x)
        for _ in range(20):
            h = Herbivore()
            h.set_default_attribute('weight')
            z=h.weight
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
        print(birth_weight_list)
        k2, p_value = stats.normaltest(birth_weight_list)
        print("k2 = {:g}".format(k2))
        print("p = {:g}".format(p_value))
        alpha = 0.01
        if p_value < alpha:
            print("The null hypothesis can be rejected")
        else:
            print("The null hypothesis cannot be rejected")

class TestProbability:
    @pytest.fixture
    def gen_animal_data(self):
        """
        Generating population of animals

        Returns
        -------
        in_cell_fauna: dict
            list of animals by their type in dictionary
        """
        parameters = {'f_max': 300.0, 'alpha': 0.3}
        s = Savannah(parameters)
        for _ in range(5):
            c = Carnivore()
            s.add_animal(c)
        for _ in range(5):
            h = Herbivore()
            s.add_animal(h)
        print(s.in_cell_fauna)
        h_count = len(s.in_cell_fauna['Herbivore'])
        c_count = len(s.in_cell_fauna['Carnivore'])
        fauna_count = h_count + c_count
        print(fauna_count)
        return s, s.in_cell_fauna, fauna_count

    def test_die(self, gen_animal_data):
        s, animals, count = gen_animal_data
        mocker = mock.Mock()
        mocker.patch('numpy.random.random', return_value =0)
        s.die_animals()
        assert count == 10
        mocker.patch('numpy.random.random', return_value =1)
        s.remove_animal()
        assert count == 9




