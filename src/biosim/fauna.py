# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from random import seed
from random import gauss
from biosim.landscapes import Landscapes
import math

class Fauna:
    def __init__(self):
        self.carni_parameters = {'eta': 0.125, 'F': 10.0, 'beta': 0.75, 'w_birth': 6.0, 'sigma_birth': 1.0, 'phi_age': 0.4, 'phi_weight':0.4, 'a_half':60, 'w_half':4.0}
        self.herbi_parameters = {'eta': 0.05, 'F': 50.0, 'beta': 0.9, 'w_birth': 8.0, 'sigma_birth': 1.5, 'phi_age': 0.2, 'phi_weight':0.1, 'a_half':40, 'w_half':10.0}
        # parameters dictionary, still need a better implimentation of it
        self.age = 0
        # initial age is zero
        # seed random number generator
        seed(1)
        # Using Gaussian values for initial weight
        self.weight_carni = gauss(self.carni_parameters['w_birth'],self.carni_parameters['sigma_birth'])
        seed(1)
        self.weight_herbi = gauss(self.herbi_parameters['w_birth'],self.herbi_parameters['sigma_birth'])
        # how to do that ????? Normal distribution of weights (what weights??)

    def grow_up(self, animal_type):
        self.age += 1
        self.decrease_weight_annual(animal_type)
        # age increase by 1 each year

    def decrease_weight_annual(self, animal_type):
        if animal_type == 'Carnivores':
            self.weight_carni -= self.weight_carni*self.carni_parameters['eta']
        elif animal_type == 'Herbivores':
            self.weight_herbi -= self.weight_herbi * self.herbi_parameters['eta']

    def increase_weight(self, animal_type, eaten_food):
        # create variable that save the aviable amount of food
        if animal_type == 'herbivores':
            self.weight_herbi += self.herbi_parameters['beta'] * eaten_food
        elif animal_type == 'carnivores':
            self.weight_carni += self.carni_parameters['beta'] * eaten_food

    def fitness(self, animal_type):
        if animal_type == 'Carnivores':
            q_age = 1/(1+math.exp^(self.carni_parameters['phi_age'])*(
                    self.age - self.carni_parameters['a_half']))
            q_weight = 1/(1+math.exp^(
                    -1*(self.carni_parameters['phi_weight'])*(
                    self.weight_carni - self.carni_parameters['w_half'])))
            self.fitness_carni = q_age * q_weight
        elif animal_type == 'Herbivores':
            q_age = 1 / (1 + math.exp ^ (self.herbi_parameters['phi_age']) * (
                        self.age - self.herbi_parameters['a_half']))
            q_weight = 1 / (1 + math.exp ^ (
                        -1 * (self.herbi_parameters['phi_weight']) * (
                            self.weight_herbi - self.herbi_parameters[
                        'w_half'])))
            self.fitness_herbi = q_age * q_weight


class Herbivores(Fauna):
    pass


class Carnivores(Fauna):
    pass


f = Fauna()
print('weight herbi: '+str(f.weight_herbi))
print('weight carni: '+str(f.weight_carni))
f.increase_weight('carnivores', 10)
print('weight herbi: '+str(f.weight_herbi))
print('weight carni: '+str(f.weight_carni))
print('fitness_carni: ' + str(f.fitness_carni(f.__class__.__name__)))