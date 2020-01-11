# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from random import seed
from random import gauss
# from biosim.landscapes import *
# That's is wrong, we can't import *
import math
import numpy as np


class Fauna:
    def __init__(self):
        """

        """
        # parameters dictionary, still need a better implimentation of it
        # cell is an object of landscape where we instantiate a new animal
        self.age = 0
        self.parameters = None
        # initial age is zero
        # Using Gaussian values for initial weight
        # how to do that ????? Normal distribution of weights (what weights??)
        self._weight = None
        self.fitness = 0

    @property
    def weight(self):
        return self._weight

    # maybe we dont need setter here
    @weight.setter
    def weight(self, value):
        self._weight = value

    def grow_up(self):
        self.age += 1
        self.decrease_weight('eta')
        # age increase by 1 each year
        # decrease the weight by the factor eta

    def decrease_weight(self, factor):
        self._weight -= self._weight * self.parameters[factor]

    #def increase_weight(self, eaten_food):
    #    # create variable that save the avialable amount of food
    #    beta = self.parameters['beta']
    #    print(self._weight)
    #    self._weight += beta * eaten_food

    #@property
    def fitness(self):
        if self._weight == 0:
            return 0
        else:
            q1 = 1 / (1 + math.exp((self.parameters['phi_age']) * (
                    self.age - self.parameters['a_half'])))
            q2 = 1 / (1 + math.exp((-1 * (self.parameters['phi_weight']) * (
                    self._weight - self.parameters['w_half']))))
            return q1 * q2

            # fitness formula
            # do we need docorator here??

    #@fitness.setter
    def fitness(self, value):
        # this is just to be used in the landscape, not needed actually
        self._fitness = value

    def migrate(self):
        pass

    @property
    def migration_probability(self):
        return self.parameters['mu'] * self.fitness
        # just return the probablity based on the equation

    @property
    def birth_probablity(self):
        nu_fauna = self.cell.nu_fauna
        zeta = self.parameters['zeta']
        w_birth = self.parameters['w_birth']
        sigma_birth = self.parameters['sigma_birth']
        if nu_fauna >= 2 and self.weight >= zeta * (w_birth * sigma_birth):
            gamma = self.parameters['gamma']
            fitness = self.fitness
            return min(1, gamma * fitness * (nu_fauna - 1))
        else:
            return 0

    def giving_birth(self):
        # now chnage the population of the cell
        # decrease the weight of the mother
        if np.random.random() > self.birth_probablity:
            # if that random number is bigger than that probablity it should
            # give birth
            self.cell.nu_fauna += 1
            self.decrease_weight('xi')
            # that's still wrong becuase it's with the weight of the baby
        else:
            pass
            # dont give birth

    @property
    def death(self):
        if self.fitness == 0:
            return 1
        else:
            return self.weight * (1 - self.fitness)


class Herbivore(Fauna):
    def __init__(self):
        seed(1)
        super().__init__()
        self.parameters = {'eta': 0.05, 'F': 50.0, 'beta': 0.9,
                           'w_birth': 8.0, 'sigma_birth': 1.5,
                           'phi_age': 0.2, 'phi_weight': 0.1,
                           'a_half': 40, 'w_half': 10.0,
                           'gamma': 0.8, 'zeta': 3.5, 'xi': 1.2,
                           'mu': 0.25}
        self._weight = gauss(self.parameters['w_birth'],
                             self.parameters['sigma_birth'])

    def eat(self, amount_to_eat):
        self._weight += self.parameters['beta']*amount_to_eat


class Carnivore(Fauna):
    def __init__(self):
        seed(1)
        super().__init__()
        self.parameters = {'eta': 0.125, 'F': 10.0, 'beta': 0.75,
                           'w_birth': 6.0, 'sigma_birth': 1.0,
                           'phi_age': 0.4, 'phi_weight': 0.4,
                           'a_half': 60, 'w_half': 4.0,
                           'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1,
                           'mu': 0.4}
        self._weight = gauss(self.parameters['w_birth'],
                             self.parameters['sigma_birth'])
