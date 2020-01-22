# -*- coding: utf-8 -*-

"""
Test set for Statistical test.
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

import pytest
from biosim.landscapes import Jungle
from biosim.fauna import Herbivore, Carnivore
from scipy import stats



class TestGaussian:
    """
    Tests that whether the birth weight is following the gaussian distribution.
    """
    @pytest.fixture
    def generate_animal_data(self):
        """
        Generates population of animals and an array of their initial weight to
        be used in test_birth_weight_dist

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
            herb = Herbivore()
            herb.set_default_weight()
            birth_weight_list.append(herb.weight)
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
        assert p_value >= alpha
        print("The null hypothesis cannot be rejected")


class TestProbability:
    """
    Tests the method die_animal as of using mock: Replacing random number
    generator with fixed value.
    """
    def test_die(self, mocker):
        """
        Tests the die_animal method and death_prob in two conditions:
        1. animal with fitness zero (herb_1).
        2. a fixed return value for random number with the use of mock (carn_1).

        Explanation of code:
        First, generating animals population for one of the landscapes types
        (i.e. jungle).
        Generating herb_1 with weight 0 to get the fitness zero and gain
        death_prob = True.
        Also, generates carn_1 with some default value just to have fixed values
        for its fitness.
        Then, use mock for numpy random number and set the return_value to it in
        the way taht it always fulfill death_prob = True for carn_1
        Finally, run the die_animal method for all of the animals of jungle
        instance and assert that the 2 animals are died and only the other 2 are
        in the animal list.

        """

        herb_1 = Herbivore(6, 0)
        herb_2 = Herbivore()
        carn_1 = Carnivore(1, 5)
        carn_2 = Carnivore()
        params = {'f_max': 10.0}
        j=Jungle(params)
        j.add_animal(carn_1)
        j.add_animal(carn_2)
        j.add_animal(herb_1)
        j.add_animal(herb_2)
        herb_1.calculate_fitness()
        assert herb_1.death_prob
        mocker.patch('numpy.random.random', return_value=0.0)
        j.die_animals()
        h_count = len(j.in_cell_fauna['Herbivore'])
        c_count = len(j.in_cell_fauna['Carnivore'])
        fauna_count = h_count + c_count
        assert fauna_count == 2

