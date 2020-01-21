
# -*- coding: utf-8 -*-

"""
Test set for landscapes class functionality and attributes.

This set of tests checks the landscapes classes methods perform as expected as per
the provided modeling.

"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

import math

import pytest
from biosim.landscapes import Desert, Ocean, Mountain, Savannah, Jungle
from biosim.fauna import Herbivore, Carnivore
from random import seed


class TestLandscapes:
    @pytest.fixture
    def gen_animal_data(self):
        seed(1)
        herb_1 = Herbivore()
        herb_2 = Herbivore()
        seed(1)
        carn_1 = Carnivore()
        carn_2 = Carnivore()
        return carn_1, carn_2, herb_1, herb_2

    @pytest.fixture
    def gen_landscape_data(self, gen_animal_data):
        landscape_params = {'f_max': 10.0}
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
        sav = gen_landscape_data['s']
        sav.save_fitness(sav.in_cell_fauna, 'Herbivore')
        assert len(sav.sorted_fauna_fitness) == 1
        assert 'Herbivore' in sav.sorted_fauna_fitness.keys()
        assert len(sav.sorted_fauna_fitness['Herbivore']) == 2
        sav.save_fitness(sav.in_cell_fauna, 'Carnivore')
        assert len(sav.sorted_fauna_fitness) == 2
        assert 'Carnivore' in sav.sorted_fauna_fitness.keys()

    def test_sort_fitness(self, gen_landscape_data):
        sav = gen_landscape_data['s']
        dict_to_sort = sav.in_cell_fauna
        sav.sort_by_fitness(dict_to_sort, 'Herbivore', False)
        dict_values = sav.sorted_fauna_fitness['Herbivore'].values()
        assert list(dict_values)[0] <= list(dict_values)[1]
        sav.sort_by_fitness(dict_to_sort, 'Carnivore')
        dict_values = sav.sorted_fauna_fitness['Carnivore'].values()
        assert list(dict_values)[0] >= list(dict_values)[1]

    def test_add_and_remove_fauna(self, gen_landscape_data):
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

    def test_mate(self, gen_landscape_data):
        jun = gen_landscape_data['j']
        mate_animal = jun.in_cell_fauna['Carnivore'][0]
        mate_animal.eat(50)
        mate_animal.eat(50)
        # increase the weight of animal
        weight_pre_birth = mate_animal.weight
        jun.mate(mate_animal)
        weight_post_birth = mate_animal.weight
        # assert len(j.fauna_objects_dict['Carnivore']) == 3
        # assert weight_post_birth < weight_pre_birth

    def test_feed_herbivore(self, gen_landscape_data):
        sav, des = (gen_landscape_data[i] for i in ('s', 'd'))
        dict_to_sort = sav.in_cell_fauna
        sav.sort_by_fitness(dict_to_sort, 'Herbivore')
        dict_keys = sav.sorted_fauna_fitness['Herbivore'].keys()
        h1_higher_fitness = list(dict_keys)[0]
        h2_lower_fitness = list(dict_keys)[1]
        h1_weight_pre_eat = h1_higher_fitness.weight
        h2_weight_pre_eat = h2_lower_fitness.weight
        assert sav.available_fodder['Herbivore'] > 0
        sav.feed_herbivore()
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
        des.feed_herbivore()
        h1_weight_post_eat = h1.weight
        h2_weight_post_eat = h2.weight
        assert des.available_fodder['Herbivore'] == 0
        assert h1_weight_post_eat == h1_weight_pre_eat
        assert h2_weight_post_eat == h2_weight_pre_eat

    def test_feed_carnivore(self, gen_landscape_data):
        sav, des = (gen_landscape_data[i] for i in ('s', 'd'))
        sav.feed_carnivore()
        # its weight remains the same meaning it doesn't eat anything

    def test_relevant_fodder(self, gen_landscape_data):
        sav, des, jun = (gen_landscape_data[i] for i in ('s', 'd', 'j'))
        herb = des.in_cell_fauna['Herbivore'][0]
        carn = des.in_cell_fauna['Carnivore'][0]
        assert jun.relevant_fodder(herb) == jun.available_fodder['Herbivore']
        assert des.relevant_fodder(herb) == des.available_fodder['Herbivore']
        assert des.relevant_fodder(herb) == 0
        assert des.relevant_fodder(carn) == sav.available_fodder['Carnivore']
        assert des.relevant_fodder(carn) == pytest.approx(
            20.10644554278285)

    def test_relative_abundance_fodder(self, gen_landscape_data):
        sav, ocean, des = (gen_landscape_data[i] for i in ('s', 'o', 'd'))
        herb = sav.in_cell_fauna['Herbivore'][0]
        carn = sav.in_cell_fauna['Carnivore'][0]
        assert des.relative_abundance_fodder(herb) == 0
        assert sav.relative_abundance_fodder(herb) == \
               pytest.approx(0.3333333333333333)
        assert ocean.relative_abundance_fodder(herb) == 0
        assert des.relative_abundance_fodder(carn) == \
               pytest.approx(0.134042970285219)

    def test_propensity(self, gen_landscape_data):
        sav, ocean, des, mount, jun = (gen_landscape_data[i]
                         for i in ('s', 'o', 'd', 'm', 'j'))
        herb = sav.in_cell_fauna['Herbivore'][0]
        carn = sav.in_cell_fauna['Carnivore'][0]
        assert sav.propensity(herb) == pytest.approx(1.3956124250860895)
        assert sav.propensity(carn) == pytest.approx(1.1434419526158457)
        assert mount.propensity(herb) == 0
        assert ocean.propensity(carn) == 0
        assert jun.propensity(herb) == pytest.approx(1.3956124250860895)
        assert des.propensity(herb) == math.exp(0) == 1
        assert des.propensity(carn) == pytest.approx(1.1434419526158457)
        assert jun.propensity(carn) == pytest.approx(1.1434419526158457)

    def test_probability_of_cell(self, gen_landscape_data):
        sav, ocean, des, mount, jun = (gen_landscape_data[i]
                         for i in ('s', 'o', 'd', 'm', 'j'))

        adj_cells = [des, des, ocean, jun]
        herb = jun.in_cell_fauna['Herbivore'][0]
        carn = jun.in_cell_fauna['Carnivore'][0]
        total_propensity_carn = sum(i.propensity(carn) for i in adj_cells)
        assert sav.probability(carn, total_propensity_carn) == \
               pytest.approx(0.33333333333333337)
        total_propensity_herb = sum(i.propensity(herb) for i in adj_cells)
        assert sav.probability(herb, total_propensity_herb) == \
               pytest.approx(0.41100462902526524)


class TestDesert(TestLandscapes):
    # test of is accessible for all of the subclasses should be added.
    def test_no_fodder(self, gen_landscape_data):
        """No fodder available in the desert"""
        ocean = gen_landscape_data['o']
        assert ocean.available_fodder['Herbivore'] == 0
        assert ocean.available_fodder['Carnivore'] == 0


class TestOcean(TestLandscapes):
    def test_number_animals(self, gen_landscape_data):
        ocean = gen_landscape_data['o']
        assert len(ocean.in_cell_fauna['Carnivore']) == 0
        assert len(ocean.in_cell_fauna['Herbivore']) == 0


class TestMountains(TestLandscapes):
    def test_number_animals(self, gen_landscape_data):
        mount = gen_landscape_data['m']
        assert len(mount.in_cell_fauna['Carnivore']) == 0
        assert len(mount.in_cell_fauna['Herbivore']) == 0


class TestSavannah(TestLandscapes):
    def test_grow_herb_fodder(self, gen_landscape_data):
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
        # the growth or the difference between them is given by the formula

    def test_reset_parameters(self, gen_landscape_data):
        sav = gen_landscape_data['s']
        alpha_pre_change = sav.parameters['alpha']
        sav.set_given_parameters({'alpha': 0.5})
        alpha_post_change = sav.parameters['alpha']
        assert alpha_post_change != alpha_pre_change


class TestJungle(TestLandscapes):
    def test_grow_herb_fodder(self, gen_landscape_data):
        jun = gen_landscape_data['j']
        assert jun.available_fodder['Herbivore'] == jun.parameters['f_max']
        assert jun.available_fodder['Herbivore'] == 10
        jun.feed_herbivore()
        fodder_pre_grow = jun.available_fodder['Herbivore']
        jun.grow_herb_fodder()
        fodder_post_grow = jun.available_fodder['Herbivore']
        assert fodder_pre_grow < fodder_post_grow
        assert fodder_post_grow == jun.parameters['f_max']
        # at the start of each simulation the fodder will have f_max
        # after a year the fodder will have f_max, no matter how much was eaten

    def test_reset_parameters(self, gen_landscape_data):
        jun = gen_landscape_data['j']
        f_max_pre_change = jun.parameters['f_max']
        jun.set_given_parameters({'f_max': 400})
        f_max_post_change = jun.parameters['f_max']
        assert f_max_post_change != f_max_pre_change
