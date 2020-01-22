
# -*- coding: utf-8 -*-

"""
Test set for landscapes class functionality and attributes.

This set of tests checks the landscapes classes methods perform as expected
as per the provided modeling.

"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

import math

import pytest
from biosim.landscapes import Desert, Ocean, Mountain, Savannah, Jungle
from biosim.fauna import Herbivore, Carnivore
from random import seed
import numpy as np


class TestLandscapes:
    @pytest.fixture
    def gen_animal_data(self):
        """
        Fixture to generate animals data to be used as input for landscape
        data

        Returns
        -------
        (carn_1, carn_2, herb_1, herb_2) : tuple
        """
        np.random.seed(1)
        herb_1 = Herbivore()
        herb_2 = Herbivore()
        np.random.seed(1)
        carn_1 = Carnivore()
        carn_2 = Carnivore()
        print(herb_1.weight, herb_2.weight)
        return carn_1, carn_2, herb_1, herb_2

    @pytest.fixture
    def gen_landscape_data(self, gen_animal_data):
        """
        generate landscape data to be used for all tests

        Parameters
        ----------
        gen_animal_data: tuple

        Returns
        -------
        landscapes_dict : dict
        """
        carn_1, carn_2, herb_1, herb_2 = gen_animal_data
        animals = {'Herbivore': [herb_1, herb_2], 'Carnivore': [carn_1, carn_2]}
        landscapes_dict = {'s': Savannah(),
                           'o': Ocean(),
                           'd': Desert(),
                           'm': Mountain(),
                           'j': Jungle()}
        for species, animals in animals.items():
            for animal in animals:
                landscapes_dict['s'].add_animal(animal)
                landscapes_dict['d'].add_animal(animal)
                landscapes_dict['j'].add_animal(animal)

        return landscapes_dict

    def test_save_fitness(self, gen_landscape_data):
        """
        check saving current life fitness of animals

        Parameters
        ----------
        gen_landscape_data: tuple

        """
        sav = gen_landscape_data['s']
        sav.save_fitness(sav.in_cell_fauna, 'Herbivore')
        assert len(sav.sorted_fauna_fitness) == 1
        assert 'Herbivore' in sav.sorted_fauna_fitness.keys()
        assert len(sav.sorted_fauna_fitness['Herbivore']) == 2
        sav.save_fitness(sav.in_cell_fauna, 'Carnivore')
        assert len(sav.sorted_fauna_fitness) == 2
        assert 'Carnivore' in sav.sorted_fauna_fitness.keys()

    def test_sort_fitness(self, gen_landscape_data):
        """
        Animals are sorted whether reverse or in ascending order

        Parameters
        ----------
        gen_landscape_data: tuple

        """
        sav = gen_landscape_data['s']
        sav.sort_by_fitness()
        herb_1 = sav.in_cell_fauna['Herbivore'][0]
        herb_2 = sav.in_cell_fauna['Herbivore'][1]
        assert herb_1.fitness <= herb_2.fitness
        carn_1 = sav.in_cell_fauna['Carnivore'][0]
        carn_2 = sav.in_cell_fauna['Carnivore'][1]
        assert carn_1.fitness >= carn_2.fitness

    def test_add_and_remove_fauna(self, gen_landscape_data):
        """
        check the length of current animals in cells after addition
        or removing

        Parameters
        ----------
        gen_landscape_data: tuple

        """
        sav, des = (gen_landscape_data[i] for i in ('s', 'd'))
        assert len(sav.in_cell_fauna['Carnivore'] + sav.in_cell_fauna[
            'Herbivore']) == 4
        assert len(des.in_cell_fauna['Herbivore']) == 2
        assert len(des.in_cell_fauna['Carnivore']) == 2
        herb_3 = Herbivore()
        sav.add_animal(herb_3)
        assert len(sav.in_cell_fauna['Carnivore'] + sav.in_cell_fauna[
            'Herbivore']) == 5
        sav.remove_animal(herb_3)
        assert len(sav.in_cell_fauna['Carnivore'] + sav.in_cell_fauna[
            'Herbivore']) == 4

    def test_feed_herbivore(self, gen_landscape_data):
        """
        weight of herbivore should increase after weight by the given formula:
        'beta' * amount_to_eat

        Parameters
        ----------
        gen_landscape_data: tuple

        """
        sav, des = (gen_landscape_data[i] for i in ('s', 'd'))
        sav.sort_by_fitness()
        h1_higher_fitness = sav.in_cell_fauna['Herbivore'][0]
        h2_lower_fitness = sav.in_cell_fauna['Herbivore'][1]
        h1_weight_pre_eat = h1_higher_fitness.weight
        h2_weight_pre_eat = h2_lower_fitness.weight
        assert sav.available_fodder['Herbivore'] > 0
        sav.feed_animals()
        assert sav.available_fodder['Herbivore'] == 0
        h1_weight_post_eat = h1_higher_fitness.weight
        h2_weight_post_eat = h2_lower_fitness.weight
        assert h1_weight_post_eat > h1_weight_pre_eat
        assert h2_weight_post_eat == h2_weight_pre_eat

        h1 = des.in_cell_fauna['Herbivore'][0]
        h2 = des.in_cell_fauna['Herbivore'][1]
        h1_weight_pre_eat = h1.weight
        h2_weight_pre_eat = h2.weight
        assert des.available_fodder['Herbivore'] == 0
        des.feed_animals()
        h1_weight_post_eat = h1.weight
        h2_weight_post_eat = h2.weight
        assert des.available_fodder['Herbivore'] == 0
        assert h1_weight_post_eat == h1_weight_pre_eat
        assert h2_weight_post_eat == h2_weight_pre_eat

    def test_relevant_fodder(self, gen_landscape_data):
        sav, des, jun = (gen_landscape_data[i] for i in ('s', 'd', 'j'))
        herb = des.in_cell_fauna['Herbivore'][0]
        carn = des.in_cell_fauna['Carnivore'][0]
        assert jun.relevant_fodder(herb) == jun.available_fodder['Herbivore']
        assert des.relevant_fodder(herb) == des.available_fodder['Herbivore']
        assert des.relevant_fodder(herb) == 0
        assert des.relevant_fodder(carn) == des.available_fodder['Carnivore']
        assert des.relevant_fodder(carn) == sum(i.weight for i in
                                                des.in_cell_fauna['Herbivore'])

    def test_relative_abundance_fodder(self, gen_landscape_data):
        """
        weight of herbivore should increase after weight by the given formula

        Parameters
        ----------
        gen_landscape_data: tuple

        """
        sav, ocean, des = (gen_landscape_data[i] for i in ('s', 'o', 'd'))
        herb = sav.in_cell_fauna['Herbivore'][0]
        assert des.relative_abundance_fodder(herb) == 0
        assert sav.relative_abundance_fodder(herb) == 10
        with pytest.raises(ValueError):
            ocean.relative_abundance_fodder(herb)

    def test_propensity(self, gen_landscape_data):
        """
        weight of herbivore should increase after weight by the given formula

        Parameters
        ----------
        gen_landscape_data: tuple

        """
        sav, ocean, des, mount, jun = (gen_landscape_data[i]
                         for i in ('s', 'o', 'd', 'm', 'j'))
        herb = sav.in_cell_fauna['Herbivore'][0]
        carn = sav.in_cell_fauna['Carnivore'][0]
        assert sav.propensity(herb) == pytest.approx(22026.465794806718)
        assert des.propensity(herb) == math.exp(0) == 1
        assert jun.propensity(herb) == pytest.approx(22026.465794806718)
        assert mount.propensity(herb) == 0
        assert ocean.propensity(carn) == 0
        assert sav.propensity(carn) == pytest.approx(1.1238862622324772)
        assert des.propensity(carn) == pytest.approx(1.1238862622324772)
        assert jun.propensity(carn) == pytest.approx(1.1238862622324772)

    def test_probability_of_cell(self, gen_landscape_data):
        """
        weight of herbivore should increase after weight by the given formula

        Parameters
        ----------
        gen_landscape_data: tuple

        """
        sav, ocean, des, mount, jun = (gen_landscape_data[i]
                         for i in ('s', 'o', 'd', 'm', 'j'))

        adj_cells = [des, des, ocean, jun]
        herb = jun.in_cell_fauna['Herbivore'][0]
        carn = jun.in_cell_fauna['Carnivore'][0]
        total_propensity_carn = sum(i.propensity(carn) for i in adj_cells)
        assert sav.probability(carn, total_propensity_carn) == \
               pytest.approx(0.3333333333333333)
        total_propensity_herb = sum(i.propensity(herb) for i in adj_cells)
        assert sav.probability(herb, total_propensity_herb) == \
               pytest.approx(0.9999092083843409)


class TestDesert(TestLandscapes):
    def test_no_fodder(self, gen_landscape_data):
        """
        No herbi fodder is available in desert

        Parameters
        ----------
        gen_landscape_data: tuple

        """
        ocean = gen_landscape_data['o']
        assert ocean.available_fodder['Herbivore'] == 0
        assert ocean.available_fodder['Carnivore'] == 0


class TestOcean(TestLandscapes):
    def test_number_animals(self, gen_landscape_data):
        """
        number of animals is zero in ocean

        Parameters
        ----------
        gen_landscape_data: tuple

        """
        ocean = gen_landscape_data['o']
        assert len(ocean.in_cell_fauna['Carnivore']) == 0
        assert len(ocean.in_cell_fauna['Herbivore']) == 0


class TestMountains(TestLandscapes):
    def test_number_animals(self, gen_landscape_data):
        """
        NUmber of animals in mountains is zero
        Parameters
        ----------
        gen_landscape_data: tuple

        """
        mount = gen_landscape_data['m']
        assert len(mount.in_cell_fauna['Carnivore']) == 0
        assert len(mount.in_cell_fauna['Herbivore']) == 0


class TestSavannah(TestLandscapes):
    def test_grow_herb_fodder(self, gen_landscape_data):
        """
        Fodder grows by the formula
        alpha * ('f_max'- available_fodder)

        Parameters
        ----------
        gen_landscape_data

        """
        sav = gen_landscape_data['s']
        assert sav.available_fodder['Herbivore'] == sav.parameters['f_max']
        assert sav.available_fodder['Herbivore'] == 10
        sav.feed_herbivore()
        fodder_pre_grow = sav.available_fodder['Herbivore']
        sav.grow_herb_fodder()
        fodder_post_grow = sav.available_fodder['Herbivore']
        assert fodder_post_grow > fodder_pre_grow
        assert fodder_post_grow - fodder_pre_grow == \
               sav.parameters['alpha'] * (sav.parameters['f_max'] -
                                        fodder_pre_grow)

    def test_reset_parameters(self, gen_landscape_data):
        """
        parameters after setting is different than default parameters
        Parameters
        ----------
        gen_landscape_data: tuple

        """
        sav = gen_landscape_data['s']
        alpha_pre_change = sav.parameters['alpha']
        sav.set_given_parameters({'alpha': 0.5})
        alpha_post_change = sav.parameters['alpha']
        assert alpha_post_change != alpha_pre_change


class TestJungle(TestLandscapes):
    def test_grow_herb_fodder(self, gen_landscape_data):
        """
        fodder become as the original value (f_max) after a year

        Parameters
        ----------
        gen_landscape_data: tuple

        """
        jun = gen_landscape_data['j']
        assert jun.available_fodder['Herbivore'] == jun.parameters['f_max']
        assert jun.available_fodder['Herbivore'] == 10
        jun.feed_herbivore()
        fodder_pre_grow = jun.available_fodder['Herbivore']
        jun.grow_herb_fodder()
        fodder_post_grow = jun.available_fodder['Herbivore']
        assert fodder_pre_grow < fodder_post_grow
        assert fodder_post_grow == jun.parameters['f_max']

    def test_reset_parameters(self, gen_landscape_data):
        """
        Reset parameter mutate the default parameters with the given
        parameters

        Parameters
        ----------
        gen_landscape_data: tuple

        """
        jun = gen_landscape_data['j']
        f_max_pre_change = jun.parameters['f_max']
        jun.set_given_parameters({'f_max': 400})
        f_max_post_change = jun.parameters['f_max']
        assert f_max_post_change != f_max_pre_change
