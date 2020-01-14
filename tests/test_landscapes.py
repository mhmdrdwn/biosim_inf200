# -*- coding: utf-8 -*-

"""
Test set for landscapes class functionality and attributes.

This set of tests checks the landscapes classes methods perform as expected as per
the provided modeling.

"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

import pytest
from biosim.landscapes import Landscapes
from biosim.landscapes import Desert, Ocean, Mountain, Savannah, Jungle
from biosim.fauna import Herbivore, Carnivore
from biosim.map import Map
from random import seed

""" is it possible now to import just biosim.landscapes as landscapes
since it's not conflicting with anything here"""


# fixtures shall be used for tests


class TestLandscapes:
    def test_geogr_map(self):
        pass
        # the sea is surrounding the island, should it be here or
        # simulation class

    # def test_consume_fodder(self):
    #  h = Herbivore()
    # l = Landscapes()
    # l.consume_fodder()
    #  assert 0 < l.available_fodder < l.required_food
    #  assert l.available_fodder == 0
    # the initial amount is f_max

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
        landscape_params = {'f_max': 30.0}
        c1, c2, h1, h2 = gen_animal_data
        animals = {'Herbivore': [h1, h2], 'Carnivore': [c1, c2]}
        s = Savannah(animals, landscape_params)
        # o = Ocean()
        d = Desert(animals)
        # m = Mountain()
        j = Jungle(animals, landscape_params)
        return s, d, j

    def test_save_fitness(self, gen_landscape_data):
        s, d, j = gen_landscape_data
        s.save_fitness(s.fauna_objects_dict, 'Herbivore')
        assert len(s.sorted_fauna_fitness) == 1
        assert 'Herbivore' in s.sorted_fauna_fitness.keys()
        assert len(s.sorted_fauna_fitness['Herbivore']) == 2
        s.save_fitness(s.fauna_objects_dict, 'Carnivore')
        assert len(s.sorted_fauna_fitness) == 2
        assert 'Carnivore' in s.sorted_fauna_fitness.keys()

    def test_sort_fitness(self, gen_landscape_data):
        s, d, j = gen_landscape_data
        dict_to_sort = s.fauna_objects_dict
        s.sort_by_fitness(dict_to_sort, 'Herbivore', False)
        dict_values = s.sorted_fauna_fitness['Herbivore'].values()
        assert list(dict_values)[0] <= list(dict_values)[1]
        s.sort_by_fitness(dict_to_sort, 'Carnivore')
        dict_values = s.sorted_fauna_fitness['Carnivore'].values()
        assert list(dict_values)[0] >= list(dict_values)[1]

    def test_add_and_remove_fauna(self, gen_landscape_data):
        s, d, j = gen_landscape_data
        assert len(s.fauna_objects_dict['Carnivore'] + s.fauna_objects_dict[
            'Herbivore']) == 4
        assert len(d.fauna_objects_dict['Herbivore']) == 2
        assert len(d.fauna_objects_dict['Carnivore']) == 2
        h3 = Herbivore()
        s.add_fauna(h3)
        assert len(s.fauna_objects_dict['Carnivore'] + s.fauna_objects_dict[
            'Herbivore']) == 5
        s.remove_fauna(h3)
        assert len(s.fauna_objects_dict['Carnivore'] + s.fauna_objects_dict[
            'Herbivore']) == 4

    def test_mate(self, gen_landscape_data):
        s, d, j = gen_landscape_data
        mate_animal = j.fauna_objects_dict['Carnivore'][0]
        mate_animal.eat(50)
        mate_animal.eat(50)
        # increase the weight of animal
        weight_pre_birth = mate_animal.weight
        j.mate(mate_animal)
        weight_post_birth = mate_animal.weight
        #assert len(j.fauna_objects_dict['Carnivore']) == 3
        #assert weight_post_birth < weight_pre_birth

    # here some other tests for other conditions of giving birth should be added after fixing the error

    def test_feed_herbivore(self, gen_landscape_data):
        s, d, j = gen_landscape_data
        dict_to_sort = s.fauna_objects_dict
        s.sort_by_fitness(dict_to_sort, 'Herbivore')
        dict_keys = s.sorted_fauna_fitness['Herbivore'].keys()
        h1_higher_fitness = list(dict_keys)[0]
        h2_lower_fitness = list(dict_keys)[1]
        h1_weight_pre_eat = h1_higher_fitness.weight
        h2_weight_pre_eat = h2_lower_fitness.weight
        assert s.available_fodder > 0
        s.feed_herbivore()
        assert s.available_fodder == 0
        h1_weight_post_eat = h1_higher_fitness.weight
        h2_weight_post_eat = h2_lower_fitness.weight
        assert h1_weight_post_eat > h1_weight_pre_eat
        assert h2_weight_post_eat == h2_weight_pre_eat

    def test_herbivore_eat_equal_fitness(self):
        # test what happen if Herbivores have same fitness
        h1 = Herbivore()
        h1.fitness = 10
        h2 = Herbivore()
        h2.fitness = 10
        animals = {'Herbivore': [h1, h2]}
        s = Savannah(animals)
        s.herbivore_eat()
        h1.parameters['F'] = 50
        h2.parameters['F'] = 50
        s.f_max = 300
        # assert s.amount_to_eat == 50 ... how can we test amount to eat?
        assert s._available_fodder == 200

    def test_herbivore_eat_in_desert(self):
        # can we move below code lines to the class that we do not need to repeat?
        # shall we do all methods in Landscapes class for all of his children seperately?
        h1 = Herbivore()
        h1.fitness = 10
        h2 = Herbivore()
        h2.fitness = 20
        c1 = Carnivore()
        c1.fitness = 30
        animals = {'Carnivore': [c1], 'Herbivore': [h1, h2]}
        d = Desert(animals)
        d.herbivore_eat()
        h1.parameters['F'] = 100
        h2.parameters['F'] = 50
        assert d._available_fodder == 0  # it breaks in the code , is there another way to test break?

    def test_carnivores_eat_no_herbi(self):
        c1 = Carnivore()
        c1.fitness = 30
        c2 = Carnivore()
        c2.fitness = 40
        c2_weight_pre_eat = c2.weight
        animals = {'Carnivore': [c1, c2], 'Herbivore': []}
        l = Landscapes(animals)
        l.carnivore_eat()
        c1.parameters['F'] = 20
        l.carnivore_eat()
        assert c2.weight == c2_weight_pre_eat
        # its weight remains the same meaning it doesn't eat anything

    def test_relevant_fodder(self):
        h1 = Herbivore()
        h1.weight = 10
        h2 = Herbivore()
        h2.weight = 20
        c1 = Carnivore()
        animals = {'Carnivore': [c1], 'Herbivore': [h1, h2]}
        s = Savannah(animals)
        assert s.relevant_fodder('Herbivore') == s._available_fodder
        # assert s.relevant_fodder('Carnivore') == 30

    def test_calculate_relative_abundance_fodder(self):
        h1 = Herbivore()
        h1.weight = 20
        h2 = Herbivore()
        h2.weight = 30
        c1 = Carnivore()
        animals = {'Carnivore': [c1], 'Herbivore': [h1, h2]}
        s = Savannah(animals)
        assert s.calculate_relative_abundance_fodder(
            'Herbivore') == 10  # which variable is return?
        # 300/((2)+1)*10  ==> 10
        assert s.calculate_relative_abundance_fodder(
            'Carnivore') == 0.5  # which variable is return?
        # 50/(1+1)50  ==> 0.5

    def test_propensity(self):
        h1 = Herbivore()
        h1.weight = 20
        h2 = Herbivore()
        h2.weight = 30
        c1 = Carnivore()
        animals = {'Carnivore': [c1], 'Herbivore': [h1, h2]}
        l = Landscapes(animals)
        assert l.propensity_to_which_cell(Herbivore, 'Mountain') == 0
        assert l.propensity_to_which_cell(Carnivore, 'Ocean') == 0

        assert l.propensity_to_which_cell(Carnivore, 'Jungle') == 1.6487212707
        assert l.propensity_to_which_cell(Herbivore, 'Desert') == 1
        assert l.propensity_to_which_cell(Herbivore, 'Jungle') == 381229223140

    def test_probability(self):
        h1 = Herbivore()
        h1.weight = 20
        h2 = Herbivore()
        h2.weight = 30
        c1 = Carnivore()
        animals = {'Carnivore': [c1], 'Herbivore': [h1, h2]}
        l = Landscapes(animals)
        map_str = """
        OOOOOOOOOOOOOOOOOOOOO
        OOOOOOOOSJJMMJJJJJJJO
        OOOOOOOOOOOOOOOOOOOOO"""

        m = Map(map_str, animals)
        map = m.create_map_dict()
        x = map.shape[1]
        y = map.shape[10]
        adj_cells = [map[x - 1, y], map[x + 1, y], map[x, y - 1],
                     map[x, y + 1]]
        l.probability_to_which_cell(animals, 'Jungle',
                                    adj_cells)


class TestDesert:
    # test of is accessible for all of the subclasses should be added.
    def test_no_fodder(self):
        """No fodder available in the desert"""
        h1 = Herbivore()
        h1.weight = 20
        h2 = Herbivore()
        h2.weight = 30
        c1 = Carnivore()
        animals = {'Carnivore': [c1], 'Herbivore': [h1, h2]}
        d = Desert(animals)
        assert d.available_fodder == 0


class TestOcean:
    def test_number_animals(self):
        fauna_objects_dict = {}
        o = Ocean(fauna_objects_dict)
        # it should be changed in the Ocean Class. because when we pass an
        # empty list it is obviouse to get an empty list as a result!!
        assert o.fauna_objects_dict == {}


class TestMountains:
    def test_number_animals(self):
        fauna_objects_dict = {}
        m = Mountain(fauna_objects_dict)
        # it should be changed in the Mountain Class. because when we pass an
        # empty list it is obviouse to get an empty list as a result!!
        assert m.fauna_objects_dict == {}


class TestSavannah:
    def test_grow_fodder_yearly(self):
        h1 = Herbivore()
        h2 = Herbivore()
        animals = {'Herbivore': [h1, h2]}
        s = Savannah(animals)
        assert s._available_fodder == s.f_max
        s.alpha = 0.5
        s.grow_fodder()
        assert s._available_fodder > s.f_max  # why s.available_fodder doesnt change? it is equal to initial amount. there is no growth!
        # post_f - pre_f == s.alpha*(s.f_max - pre_f)
        # the growth or the difference between them is given by the formula
        s.alpha = 0
        s.grow_fodder()
        assert s._available_fodder == s.f_max  # testing if coeficient is zero


class TestJungle:
    def test_grow_fodder_yearly(self):
        h1 = Herbivore()
        h2 = Herbivore()
        animals = {'Herbivore': [h1, h2]}
        j = Jungle(animals)
        assert j.available_fodder == j.f_max
        j.grow_fodder()
        assert j.available_fodder == j.f_max
        # at the start of each simulation the fodder will have f_max
        # after a year the fodder will have f_max, no matter how much was eaten
