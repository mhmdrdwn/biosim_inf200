# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from random import seed
from random import gauss
from biosim.landscapes import Landscapes
class Fauna:
    def __init__(self):
        self.carni_parameters = {'eta': 0.125, 'F': 10.0, 'beta': 0.75, 'w_birth': 6.0, 'sigma_birth': 1.0}
        self.herbi_parameters = {'eta': 0.05, 'F': 50.0, 'beta': 0.9, 'w_birth': 8.0, 'sigma_birth': 1.5}
        # parameters dictionary, still need a better implimentation of it
        self.age = 0
        # initial age is zero
        # seed random number generator
        seed(1)
        # Using Gaussian values for initial weight
        self.weight_carni = gauss(self.carni_parameters['w_birth'],self.carni_parameters['sigma_birth'])
        self.weight_herbi = gauss(self.herbi_parameters['w_birth'],self.herbi_parameters['sigma_birth'])
        # how to do that ????? Normal distribution of weights (what weights??)

    def grow_up(self):
        self.age += 1
        self.decrease_weight_annual()
        # age increase by 1 each year

    def decrease_weight_annual(self):
        self.weight_carni -= self.weight_carni*self.carni_parameters['eta']
        self.weight_herbi -= self.weight_herbi * self.herbi_parameters['eta']
        # that's just for carni, still need to code herbi

    def increase_weight(self, eaten_food, animal_type):
        # create variable that save the aviable amount of food
        self.weight_herbi += self.herbi_parameters[
                                 'beta'] * eaten_food
        self.weight_carni += self.carni_parameters[
                                 'beta'] * eaten_food

        # that's just for carni, still need to code herbi


class Herbivores(Fauna):
    def --init--(self,available_food):
        super() self.available_food

    def eat(self):
        if available_food > 0:
            if self.herbi_parameters['F'] <= available_food:
                self.weight_herbi += self.herbi_parameters['beta']*self.herbi_parameters['F']
            else:
                self.weight_herbi += self.herbi_parameters['beta']*self.available_food

class Carnivores(Fauna):
    available_food = {'carni_food': self.weight_herbi,
                      'herbi_food': Landscapes.available_fodder}
    if available_food > 0:
        if self.carni_parameters['F'] <= available_food:
            self.weight_carni += self.carni_parameters['beta'] * \
                                 self.carni_parameters['F']
        else:
            self.weight_carni += self.carni_parameters[
                                     'beta'] * self.available_food


f = Fauna()

