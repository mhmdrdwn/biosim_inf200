# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from random import seed
from random import gauss
from biosim.landscapes import *
# That's is wrong
import math


class Fauna:
    def __init__(self, cell):
        # parameters dictionary, still need a better implimentation of it
        self.cell = cell
        # cell is an object of landscape where we instantiate a new animal
        self.age = 0
        self.parameters = None
        # initial age is zero
        # Using Gaussian values for initial weight
        self.weight = None
        # how to do that ????? Normal distribution of weights (what weights??)
        self.fitness = None
        self.death_probability = None
        self.birth_probability = None

    def grow_up(self):
        self.age += 1
        self.decrease_weight('eta')
        # age increase by 1 each year
        # decresae the weight by the factor eta

    def decrease_weight(self, factor):
        self.weight -= self.weight * self.parameters[factor]

    def increase_weight(self, eaten_food):
        # create variable that save the avialable amount of food
        beta = self.parameters['beta']
        self.weight += beta * eaten_food

    def calculate_fitness(self):
        if self.weight == 0:
            self.fitness = 0
        else:
            q1 = 1 / (1 + math.exp((self.parameters['phi_age']) * (
                    self.age - self.parameters['a_half'])))
            q2 = 1 / (1 + math.exp((-1 * (self.parameters['phi_weight']) * (
                    self.weight - self.parameters['w_half']))))
            self.fitness = q1 * q2

            # fitness formula
            # do we need docorator here??

    def migration(self):
        pass

    def calculate_birth_probability(self):
        nu_fauna = self.cell.nu_fauna
        zeta = self.parameters['zeta']
        w_birth = self.parameters['w_birth']
        sigma_birth = self.parameters['sigma_birth']
        if nu_fauna >= 2 and self.weight >= zeta*(w_birth*sigma_birth):
            gamma = self.parameters['gamma']
            fitness = self.fitness
            self.birth_probability = min(1, gamma * fitness * (nu_fauna - 1))
        else:
            self.birth_probability = 0

    def giving_birth(self):
        # now chnage the population of the cell
        # decrease the weight of the mother
        self.cell.nu_fauna += 1
        self.decrease_weight('xi')
        # that's still wrong becuase it's with the weight of the baby

    def calculate_death(self):
        if self.fitness == 0:
            self.death_probability = 1
        else:
            self.death_probability = self.weight * (1 - self.fitness)


class Herbivores(Fauna):
    def __init__(self, cell):
        seed(1)
        super().__init__(cell)
        self.parameters = {'eta': 0.05, 'F': 50.0, 'beta': 0.9,
                           'w_birth': 8.0, 'sigma_birth': 1.5,
                           'phi_age': 0.2, 'phi_weight': 0.1,
                           'a_half': 40, 'w_half': 10.0,
                           'gamma': 0.8, 'zeta': 3.5, 'xi': 1.2}
        self.weight = gauss(self.parameters['w_birth'],
                            self.parameters['sigma_birth'])


class Carnivores(Fauna):
    def __init__(self, cell):
        seed(1)
        super().__init__(cell)
        self.parameters = {'eta': 0.125, 'F': 10.0, 'beta': 0.75,
                           'w_birth': 6.0, 'sigma_birth': 1.0,
                           'phi_age': 0.4, 'phi_weight': 0.4,
                           'a_half': 60, 'w_half': 4.0,
                           'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1}
        self.weight = gauss(self.parameters['w_birth'],
                            self.parameters['sigma_birth'])


_cell = Savannah()
_cell.nu_fauna = 3
c = Carnivores(_cell)
h = Herbivores(_cell)
print(c)
print(h)
print('weight herbi: ' + str(h.weight))
print('weight carni: ' + str(c.weight))
print('###############')
c.increase_weight(10)
print('weight herbi: ' + str(h.weight))
print('weight carni: ' + str(c.weight))
print('###############')
h.decrease_weight('eta')
c.decrease_weight('eta')
print('weight herbi: ' + str(h.weight))
print('weight carni: ' + str(c.weight))
print('age herbi: ' + str(h.age))
print('age carni: ' + str(c.age))
print('###############')
h.grow_up()
h.grow_up()
c.grow_up()
print('weight herbi: ' + str(h.weight))
print('weight carni: ' + str(c.weight))
print('age herbi: ' + str(h.age))
print('age carni: ' + str(c.age))
print('###############')
c.calculate_fitness()
print('fitness: ' + str(c.fitness))
c.calculate_death()
print('death prob: ' + str(c.death_probability))
# print('fitness_carni: ' + str(f.fitness_carni(f.__class__.__name__)))
c.calculate_birth_probability()
print('birth prob: ' + str(c.birth_probability))