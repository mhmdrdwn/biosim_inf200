# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from biosim.fauna import Fauna
from biosim.fauna import Herbivores
from biosim.fauna import Carnivores


class Landscapes:
    def __init__(self, available_fodder):
        self.available_fodder = 0
        self.nu_fauna = 0
        self.required_food = 0


    def consume_fodder(self):
        eaten_food = 0
        self.required_food = Herbivores(cell).parameters['F']
        if self.required_food <= self.available_fodder:
            eaten_food = self.required_food
            self.available_fodder -= self.required_food
        else:
            eaten_food = self.available_fodder
            self.available_fodder = 0

        return eaten_food,self.available_fodder


class Savannah(Landscapes):
    def __init__(self,available_fodder, is_accessible, f_max, alpha):
        available_fodder = self.available_fodder
        self.is_accessible = True
        self.alpha = 0.3
        self.f_max = 300

    def grow_fodder_annual(self):
        self.available_fodder += self.alpha*(self.f_max-self.available_fodder)
        return self.available_fodder


class Jungle(Landscapes):
    def __init__(self, available_fodder, is_accessible, f_max):
        available_fodder = self.available_fodder
        self.is_accessible = True
        self.f_max = 800

    def grow_fodder_annual(self):
        self.available_fodder = self.f_max
        return self.available_fodder

class Desert(Landscapes):
    def __init__(self, available_fodder, is_accessible):
        self.available_fodder = 0
        self.is_accessible = True
        # That's because it's not changeable, so it's private variable


class Mountains(Landscapes):
    def __init__(self, available_fodder, is_accessible):
        self.available_fodder = 0
        self.is_accessible = False
        # That's because it's not changeable, so it's private variable


class Ocean(Landscapes):
    def __init__(self, available_fodder, is_accessible):
        self.available_fodder = 0
        self.is_accessible = False
        # That's because it's not changeable, so it's private variable
