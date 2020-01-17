# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from random import gauss
import math
import numpy as np
from random import seed


class Fauna:
    # this should be a base class
    parameters = {}

    def __init__(self, age=None, weight=None):
        """

        """
        #self.age = None
        #self._weight = None

        if age is None:
            self.set_default_attribute('age')
        else:
            self.protect_against_non_valid_attribute('Age', age)
            self.age = age

        if weight is None:
            self.set_default_attribute('weight')
        else:
            self.protect_against_non_valid_attribute('Weight', weight)
            self._weight = weight

        self._fitness = 0

    @staticmethod
    def protect_against_non_valid_attribute(attribute_name, attribute):
        if not isinstance(attribute, (int, float)):
            raise ValueError(attribute_name + ' of animal can\'t be set to '
                             + attribute_name +
                             ', it has to be integer or float')

    def set_default_attribute(self, attribute_name):
        # default attributes are the birth weight and birth age
        if attribute_name is 'weight':
            self._weight = gauss(self.parameters['w_birth'],
                                 self.parameters['sigma_birth'])
        if attribute_name is 'age':
            self.age = 0

    @property
    def weight(self):
        return self._weight

    def grow_up(self):
        self.age += 1
        weight_to_reduce = self._weight * self.parameters['eta']
        self.reduce_weight(weight_to_reduce)
        # age increase by 1 each year
        # decrease the weight by the factor eta

    def reduce_weight(self, amount_to_reduce):
        self._weight -= amount_to_reduce

    @property
    def fitness(self):
        self.calculate_fitness()
        return self._fitness

    @staticmethod
    def fitness_formula(age, weight, parameters):
        # fitness formula
        q1 = 1 / (1 + math.exp((parameters['phi_age'])
                               * (age - parameters['a_half'])))
        q2 = 1 / (1 + math.exp((-1 * (parameters['phi_weight'])
                                * (weight - parameters['w_half']))))
        return q1*q2

    def calculate_fitness(self):
        # this is a class method because the formula is fixed for all animals
        if self._weight == 0:
            self._fitness = 0
        else:
            self._fitness = self.fitness_formula(
                self.age, self._weight, self.parameters)

    @property
    def move_probability(self):
        return self.parameters['mu'] * self.fitness
        # animal move probablity based on the equation

    # @property
    def birth_probablity(self, num_fauna):
        zeta = self.parameters['zeta']
        w_birth = self.parameters['w_birth']
        sigma_birth = self.parameters['sigma_birth']
        if num_fauna >= 2 and self.weight >= zeta * (w_birth + sigma_birth):
            gamma = self.parameters['gamma']
            return min(1, gamma * self.fitness * (num_fauna - 1))
        else:
            return 0

    def give_birth(self, baby):

        self._weight -= baby.weight * baby.parameters['xi']

    # @property
    def death_probability(self):
        if self.fitness == 0:
            return 1
        else:
            return self.parameters['omega'] * (1 - self.fitness)

    def eat(self, amount_to_eat):
        self._weight += self.parameters['beta'] * amount_to_eat
        # the same behaviour for both carni and herbi, just the difference
        # is in the amount to eat


class Herbivore(Fauna):
    parameters = {'eta': 0.05, 'F': 10.0, 'beta': 0.9, 'w_birth': 8.0,
                  'sigma_birth': 1.5, 'phi_age': 0.2, 'phi_weight': 0.1,
                  'a_half': 40, 'w_half': 10.0, 'gamma': 0.8, 'zeta': 3.5,
                  'xi': 1.2, 'mu': 0.25, 'lambda': 1.0, 'omega': 0.4}

    def __init__(self, age=None, weight=None, params=None):
        super().__init__(age, weight)
        if params is not None:
            # if we have given any subset of new parameters, we are going to
            # call that function that will overwrite the default parameters
            self.set_given_parameters(params)
            # and after that we set the new updated class variable to the attribute
        self.parameters = Herbivore.parameters

    @staticmethod
    def set_given_parameters(given_parameters):
        for parameter in given_parameters:
            if parameter in Herbivore.parameters:
                if parameter == 'eta' and given_parameters[parameter] > 1:
                    raise ValueError('Illegal parameter value, ' +
                                     str(parameter) + ' can\'t be more than 1')
                elif given_parameters[parameter] < 0:
                    # protect against negative values
                    raise ValueError('Illegal parameter value, ' +
                                     str(parameter) + ' can\'t be negative')
                else:
                    # if given_parameters[parameter] >= 0
                    Herbivore.parameters[parameter] = \
                        given_parameters[parameter]
            else:
                # unknown parameter
                raise RuntimeError('Unknown parameter, ' + str(parameter) +
                                   ' can\'t be set')


class Carnivore(Fauna):
    parameters = {'eta': 0.125, 'F': 50.0, 'beta': 0.75, 'w_birth': 6.0,
                  'sigma_birth': 1.0, 'phi_age': 0.4, 'phi_weight': 0.4,
                  'a_half': 60, 'w_half': 4.0, 'gamma': 0.8, 'zeta': 3.5,
                  'xi': 1.1, 'mu': 0.4, 'DeltaPhiMax': 10.0, 'lambda': 1.0,
                  'omega': 0.9}

    def __init__(self, age=None, weight=None, params=None):
        super().__init__(age, weight)
        self._kill_probablity = None
        if params is not None:
            # if we have given any subset of new parameters, we are going to
            # call that function that will overwrite the default parameters
            self.set_given_parameters(params)
            # and after that we set the new updated class variable to the attribute
        self.parameters = Carnivore.parameters

    @staticmethod
    def set_given_parameters(given_parameters):
        for parameter in given_parameters:
            if parameter in Carnivore.parameters:
                if parameter == 'eta' and given_parameters[parameter] > 1:
                    raise ValueError('Illegal parameter value, eta '
                                     'can\'t be more than 1')
                elif given_parameters[parameter] <= 0:
                    # protect against negative values
                    raise ValueError('Illegal parameter value, ' +
                                     str(parameter) + ' can\'t be zero or '
                                                      'negative')
                else:
                    # if given_parameters[parameter] >= 0
                    Carnivore.parameters[parameter] = \
                        given_parameters[parameter]
            else:
                # unknown parameter
                raise RuntimeError('Unknown parameter, ' + str(parameter) +
                                   ' can\'t be set')

    # @property
    def kill_probablity(self, herbivore_to_kill):
        if self.fitness <= herbivore_to_kill.fitness:
            self._kill_probablity = 0
        elif 0 < self.fitness - herbivore_to_kill.fitness < self.parameters[
            'DeltaPhiMax']:
            self._kill_probablity = (self.fitness -
                                     herbivore_to_kill.fitness) / \
                                    self.parameters['DeltaPhiMax']
        else:
            self._kill_probablity = 1
        return self._kill_probablity


if __name__ == '__main__':
    c = Carnivore()
    print(c.age)
    print(c.weight)