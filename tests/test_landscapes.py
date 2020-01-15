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

    def test_save_fitness(self, gen_landscape_data):
        s = gen_landscape_data['s']
        s.save_fitness(s.in_cell_fauna, 'Herbivore')
        assert len(s.sorted_fauna_fitness) == 1
        assert 'Herbivore' in s.sorted_fauna_fitness.keys()
        assert len(s.sorted_fauna_fitness['Herbivore']) == 2
        s.save_fitness(s.in_cell_fauna, 'Carnivore')
        assert len(s.sorted_fauna_fitness) == 2
        assert 'Carnivore' in s.sorted_fauna_fitness.keys()

    def test_sort_fitness(self, gen_landscape_data):
        s = gen_landscape_data['s']
        dict_to_sort = s.in_cell_fauna
        s.sort_by_fitness(dict_to_sort, 'Herbivore', False)
        dict_values = s.sorted_fauna_fitness['Herbivore'].values()
        assert list(dict_values)[0] <= list(dict_values)[1]
        s.sort_by_fitness(dict_to_sort, 'Carnivore')
        dict_values = s.sorted_fauna_fitness['Carnivore'].values()
        assert list(dict_values)[0] >= list(dict_values)[1]

    def test_add_and_remove_fauna(self, gen_landscape_data):
        s, d = (gen_landscape_data[i] for i in ('s', 'd'))
        assert len(s.in_cell_fauna['Carnivore'] + s.in_cell_fauna[
            'Herbivore']) == 4
        assert len(d.in_cell_fauna['Herbivore']) == 2
        assert len(d.in_cell_fauna['Carnivore']) == 2
        h3 = Herbivore()
        s.add_fauna(h3)
        assert len(s.in_cell_fauna['Carnivore'] + s.in_cell_fauna[
            'Herbivore']) == 5
        s.remove_fauna(h3)
        assert len(s.in_cell_fauna['Carnivore'] + s.in_cell_fauna[
            'Herbivore']) == 4

    def test_mate(self, gen_landscape_data):
        j = gen_landscape_data['j']
        mate_animal = j.in_cell_fauna['Carnivore'][0]
        mate_animal.eat(50)
        mate_animal.eat(50)
        # increase the weight of animal
        weight_pre_birth = mate_animal.weight
        j.mate(mate_animal)
        weight_post_birth = mate_animal.weight
        # assert len(j.fauna_objects_dict['Carnivore']) == 3
        # assert weight_post_birth < weight_pre_birth

    def test_feed_herbivore(self, gen_landscape_data):
        s, d = (gen_landscape_data[i] for i in ('s', 'd'))
        dict_to_sort = s.in_cell_fauna
        s.sort_by_fitness(dict_to_sort, 'Herbivore')
        dict_keys = s.sorted_fauna_fitness['Herbivore'].keys()
        h1_higher_fitness = list(dict_keys)[0]
        h2_lower_fitness = list(dict_keys)[1]
        h1_weight_pre_eat = h1_higher_fitness.weight
        h2_weight_pre_eat = h2_lower_fitness.weight
        assert s.available_fodder['Herbivore'] > 0
        s.feed_herbivore()
        assert s.available_fodder['Herbivore'] == 0
        h1_weight_post_eat = h1_higher_fitness.weight
        h2_weight_post_eat = h2_lower_fitness.weight
        assert h1_weight_post_eat > h1_weight_pre_eat
        assert h2_weight_post_eat == h2_weight_pre_eat

        h1 = d.in_cell_fauna['Herbivore'][0]
        h2 = d.in_cell_fauna['Herbivore'][1]
        h1_weight_pre_eat = h1.weight
        h2_weight_pre_eat = h2.weight
        assert d.available_fodder['Herbivore'] == 0
        d.feed_herbivore()
        h1_weight_post_eat = h1.weight
        h2_weight_post_eat = h2.weight
        assert d.available_fodder['Herbivore'] == 0
        assert h1_weight_post_eat == h1_weight_pre_eat
        assert h2_weight_post_eat == h2_weight_pre_eat

    def test_feed_carnivore(self, gen_landscape_data):
        s, d = (gen_landscape_data[i] for i in ('s', 'd'))
        s.feed_carnivore()
        # its weight remains the same meaning it doesn't eat anything

    def test_relevant_fodder(self, gen_landscape_data):
        s, d, j = (gen_landscape_data[i] for i in ('s', 'd', 'j'))
        herb = d.in_cell_fauna['Herbivore'][0]
        carn = d.in_cell_fauna['Carnivore'][0]
        assert s.relevant_fodder(herb, j) == j.available_fodder['Herbivore']
        assert s.relevant_fodder(herb, d) == d.available_fodder['Herbivore']
        assert s.relevant_fodder(herb, d) == 0
        assert s.relevant_fodder(carn, d) == s.available_fodder['Carnivore']
        assert s.relevant_fodder(carn, d) == pytest.approx(
            20.10644554278285)

    def test_relative_abundance_fodder(self, gen_landscape_data):
        s, o, d = (gen_landscape_data[i] for i in ('s', 'o', 'd'))
        herb = s.in_cell_fauna['Herbivore'][0]
        carn = s.in_cell_fauna['Carnivore'][0]
        assert s.relative_abundance_fodder(herb, d) == 0
        assert s.relative_abundance_fodder(herb, o) == 0
        assert s.relative_abundance_fodder(carn, d) == pytest.approx(
            0.134042970285219)
        assert s.relative_abundance_fodder(carn, o) == 0

    def test_propensity(self, gen_landscape_data):
        s, o, d, m, j = (gen_landscape_data[i]
                         for i in ('s', 'o', 'd', 'm', 'j'))
        herb = s.in_cell_fauna['Herbivore'][0]
        carn = s.in_cell_fauna['Carnivore'][0]
        assert s.propensity(herb, m) == 0
        assert s.propensity(carn, o) == 0
        assert s.propensity(herb, j) == pytest.approx(1.3956124250860895)
        assert s.propensity(herb, d) == math.exp(0)
        assert s.propensity(carn, d) == pytest.approx(1.1434419526158457)
        assert s.propensity(carn, j) == pytest.approx(1.1434419526158457)


class TestDesert(TestLandscapes):
    # test of is accessible for all of the subclasses should be added.
    def test_no_fodder(self, gen_landscape_data):
        """No fodder available in the desert"""
        o = gen_landscape_data['o']
        assert o.available_fodder['Herbivore'] == 0
        assert o.available_fodder['Carnivore'] == 0


class TestOcean(TestLandscapes):
    def test_number_animals(self, gen_landscape_data):
        o = gen_landscape_data['o']
        assert len(o.in_cell_fauna['Carnivore']) == 0
        assert len(o.in_cell_fauna['Herbivore']) == 0
        # it should be changed in the Ocean Class. because when we pass an
        # empty list it is obviouse to get an empty list as a result!!
        with pytest.raises(ValueError) as err:
            Ocean({'Herbivore': [Herbivore()]})
        assert err.type is ValueError


class TestMountains(TestLandscapes):
    def test_number_animals(self, gen_landscape_data):
        m = gen_landscape_data['m']
        assert len(m.in_cell_fauna['Carnivore']) == 0
        assert len(m.in_cell_fauna['Herbivore']) == 0
        # it should be changed in the Mountain Class. because when we pass an
        # empty list it is obviouse to get an empty list as a result!!
        with pytest.raises(ValueError) as err:
            Mountain({'Herbivore': [Herbivore()]})
        assert err.type is ValueError


class TestSavannah(TestLandscapes):
    def test_grow_herb_fodder(self, gen_landscape_data):
        s = gen_landscape_data['s']
        assert s.available_fodder['Herbivore'] == s.parameters['f_max']
        assert s.available_fodder['Herbivore'] == 10
        s.feed_herbivore()
        fodder_pre_grow = s.available_fodder['Herbivore']
        s.grow_herb_fodder()
        fodder_post_grow = s.available_fodder['Herbivore']
        assert fodder_post_grow > fodder_pre_grow
        assert fodder_post_grow - fodder_pre_grow == \
               s.parameters['alpha'] * (s.parameters['f_max'] -
                                        fodder_pre_grow)
        # the growth or the difference between them is given by the formula

    def test_reset_parameters(self, gen_landscape_data):
        s = gen_landscape_data['s']
        alpha_pre_change = s.parameters['alpha']
        s.set_given_parameters({'alpha': 0.5})
        alpha_post_change = s.parameters['alpha']
        assert alpha_post_change != alpha_pre_change


class TestJungle(TestLandscapes):
    def test_grow_herb_fodder(self, gen_landscape_data):
        j = gen_landscape_data['j']
        assert j.available_fodder['Herbivore'] == j.parameters['f_max']
        assert j.available_fodder['Herbivore'] == 10
        j.feed_herbivore()
        fodder_pre_grow = j.available_fodder['Herbivore']
        j.grow_herb_fodder()
        fodder_post_grow = j.available_fodder['Herbivore']
        assert fodder_pre_grow < fodder_post_grow
        assert fodder_post_grow == j.parameters['f_max']
        # at the start of each simulation the fodder will have f_max
        # after a year the fodder will have f_max, no matter how much was eaten

    def test_reset_parameters(self, gen_landscape_data):
        s, d, j, o, m = gen_landscape_data
        f_max_pre_change = s.parameters['f_max']
        s.set_given_parameters({'f_max': 400})
        f_max_post_change = s.parameters['f_max']
        assert f_max_post_change != f_max_pre_change
