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


    def test_number_animals(self):
        h1 = Herbivore()
        h2 = Herbivore()
        c1 = Carnivore()
        animals = {'Carnivore': [c1], 'Herbivore': [h1, h2]}
        s = Savannah(animals)
        assert len(s.fauna_objects_dict['Carnivore']+s.fauna_objects_dict['Herbivore']) == 3
        h3 = Herbivore()
        s.add_fauna(h3)
        assert len(s.fauna_objects_dict['Carnivore']+s.fauna_objects_dict['Herbivore']) == 4
        s.remove_fauna(c1)
        assert len(s.fauna_objects_dict['Carnivore'] + s.fauna_objects_dict[
            'Herbivore']) == 3

    def test_give_birth(self):
        h1 = Herbivore()
        h1.weight = 20
        h2 = Herbivore()
        h2.weight = 30
        c1 = Carnivore()
        animals = {'Carnivore': [c1], 'Herbivore': [h1, h2]}
        l = Landscapes(animals)
        l.give_birth(c1)
        assert len(l.fauna_objects_dict['Carnivore']+l.fauna_objects_dict['Herbivore']) == 3
    # here some other tests for other conditions of giving birth should be added after fixing the error

    def test_herbivore_eat(self):
        h1 = Herbivore()
        h1.fitness = 10
        h2 = Herbivore()
        h2.fitness = 20
        c1 = Carnivore()
        c1.fitness = 30
        animals = {'Carnivore': [c1], 'Herbivore': [h1, h2]}
        s = Savannah(animals)
        assert h1.parameters['F'] == 50
        s.herbivore_eat()
        c1.parameters['F'] = 20  #add carnivores to test if the code doesn't include this type and only includes Herbivores type
        s.f_max = 300
        # assert s.amount_to_eat == 50 ... how can we test amount to eat?
        assert s._available_fodder == 200
        s.herbivore_eat()
        assert s._available_fodder == 100


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
        assert d._available_fodder == 0   # it breaks in the code , is there another way to test break?

    def test_carnivores_eat_no_herbi(self):
        c1 = Carnivore()
        c1.fitness = 30
        c2 = Carnivore()
        c2.fitness = 40
        animals = {'Carnivore': [c1, c2]}
        l = Landscapes(animals)
        l.carnivore_eat()
        c1.parameters['F'] = 20
        assert l.carnivore_eat()==0
        #assert what variable
        # it breaks in the code , is there another way to test break?

    def test_relevant_fodder(self):
        h1 = Herbivore()
        h1.weight = 10
        h2 = Herbivore()
        h2.weight = 20
        c1 = Carnivore()
        animals = {'Carnivore': [c1], 'Herbivore': [h1, h2]}
        s = Savannah(animals)
        assert s.relevant_fodder('Herbivore') == s._available_fodder
        assert s.relevant_fodder('Carnivore') == 30

    def test_calculate_relative_abundance_fodder(self):
        h1 = Herbivore()
        h1.weight = 20
        h2 = Herbivore()
        h2.weight = 30
        c1 = Carnivore()
        animals = {'Carnivore': [c1], 'Herbivore': [h1, h2]}
        s = Savannah(animals)
        assert s.calculate_relative_abundance_fodder('Herbivore')  == 10   # which variable is return?
        # 300/((2)+1)*10  ==> 10
        assert  s.calculate_relative_abundance_fodder('Carnivore')  == 0.5   # which variable is return?
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

        m= Map(map_str, animals )
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
        #post_f - pre_f == s.alpha*(s.f_max - pre_f)
        # the growth or the difference between them is given by the formula
        s.alpha = 0
        s.grow_fodder()
        assert s._available_fodder ==  s.f_max  # testing if coeficient is zero




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


