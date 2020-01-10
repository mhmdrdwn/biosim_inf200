# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from biosim.fauna import Fauna
from biosim.fauna import Herbivores
from biosim.fauna import Carnivores


class Landscapes:
    def __init__(self, fauna_objects_list):
        self._available_fodder = 0
        # those fauna list is given from the map, which was given earlier
        # from the simulation as initial animals and we append it to when
        # migration and birthing
        self.fauna_objects_list = fauna_objects_list

    def change_fodder_amount(self):
        # change the amount of avialable fadder in landscape after animal eats
        eaten_food = 0
        required_food = Herbivores(cell).parameters['F']
        if required_food <= self.available_fodder:
            eaten_food = required_food
            self._available_fodder -= required_food
        else:
            eaten_food = self.available_fodder
            self._available_fodder = 0

        return eaten_food, self.available_fodder

    @property
    def available_fodder(self):
        return self._available_fodder
    # why that???

class Savannah(Landscapes):
    is_accessible = True

    def __init__(self, fauna_objects_list):
        super().__init__(fauna_objects_list)
        self.alpha = 0.3
        self.f_max = 300
        self._available_fodder = self.f_max
        # aviable fodder equals to f_max at the beginning of
        # instaniating anew object

    def grow_fodder_annual(self):
        self._available_fodder += self.alpha * (self.f_max -
                                                self._available_fodder)


class Jungle(Landscapes):
    is_accessible = True

    def __init__(self, fauna_objects_list):
        super().__init__(fauna_objects_list)
        self.f_max = 800
        self._available_fodder = self.f_max
        # amount of initial fodder aviable should equals to f_max

    def grow_fodder_annual(self):
        self._available_fodder = self.f_max


class Desert(Landscapes):
    is_accessible = True

    def __init__(self, fauna_objects_list):
        super().__init__(fauna_objects_list)
        self._available_fodder = 0
        # should we move aviable_fodder to the class level

        # That's because it's not changeable, so it's private variable


class Mountain(Landscapes):
    available_fodder = 0
    fauna_objects_list = []
    is_accessible = False

    # That's because it's not changeable, so it's private variable, fixed
    # class variabels for all classes


class Ocean(Landscapes):
    available_fodder = 0
    fauna_objects_list = []
    is_accessible = False
    # That's because it's not changeable, so it's private variable
    # those are instance variables becuase they are fixed for all
    # instances of the class, meaning if those value changes, they will
    # chnaged in all instances of the variables


# testing
animals = ['1', '2']
l = Savannah(animals)
print(l.fauna_objects_list)
print(l.available_fodder)
print('###########')
l = Jungle(animals)
print(l.fauna_objects_list)
print(l.available_fodder)
print('###########')
l = Ocean(animals)
print(l.fauna_objects_list)
print(l.available_fodder)