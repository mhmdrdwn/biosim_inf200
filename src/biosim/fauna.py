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
    def __init__(self, given_parameters=None):
        """

        """
        self.given_parameters = given_parameters
        self.age = 0
        # initial age is zero
        self.parameters = None
        # Using Gaussian values for initial weight
        # how to do that ????? Normal distribution of weights (what weights??)
        self._weight = None
        self._fitness = 0

    @property
    def weight(self):
        return self._weight

    # maybe we dont need setter here
    @weight.setter
    def weight(self, value):
        self._weight = value

    def grow_up(self):
        self.age += 1
        self._weight -= self._weight*self.parameters['eta']
        # age increase by 1 each year
        # decrease the weight by the factor eta

    # def increase_weight(self, eaten_food):
    #    # create variable that save the avialable amount of food
    #    beta = self.parameters['beta']
    #    print(self._weight)
    #    self._weight += beta * eaten_food

    @property
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

    @fitness.setter
    def fitness(self, value):
        # this is just to be used in the landscape, not needed actually
        self._fitness = value

    @property
    def move_probability(self):
        return self.parameters['mu'] * self._fitness
        # animal move probablity based on the equation

    @property
    def birth_probablity(self, num_fauna):
        zeta = self.parameters['zeta']
        w_birth = self.parameters['w_birth']
        sigma_birth = self.parameters['sigma_birth']
        if num_fauna >= 2 and self.weight >= zeta * (w_birth * sigma_birth):
            gamma = self.parameters['gamma']
            fitness = self.fitness
            return min(1, gamma * fitness * (num_fauna - 1))
        else:
            return 0

    @property
    def death_probability(self):
        if self.fitness == 0:
            return 1
        else:
            return self.weight * (1 - self.fitness)

    def die(self):
        # if np.random.random() is more than the probability , then die
        # del self
        pass
        # delete itself, but we dont need this

    def eat(self, amount_to_eat):
        self._weight += self.parameters['beta'] * amount_to_eat
        # the same behaviour for both carni and herbi, just the difference
        # is in the amount to eat


class Herbivore(Fauna):
    parameters = {'eta': 0.05, 'F': 50.0, 'beta': 0.9, 'w_birth': 8.0,
                  'sigma_birth': 1.5, 'phi_age': 0.2, 'phi_weight': 0.1,
                  'a_half': 40, 'w_half': 10.0,'gamma': 0.8, 'zeta': 3.5,
                  'xi': 1.2, 'mu': 0.25, 'lambda': 1.0}

    def __init__(self, given_parameters=None):
        super().__init__(given_parameters)
        if given_parameters is not None:
            # if we have given any subset of new parameters, we are going to
            # call that function that will overwrite the default parameters
            self.set_given_parameters(given_parameters)
            # and after that we set the new updated class variable to the attribute
        self.parameters = Herbivore.parameters
        self._weight = gauss(self.parameters['w_birth'],
                             self.parameters['sigma_birth'])

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
                    #if given_parameters[parameter] >= 0
                    Herbivore.parameters[parameter] = \
                        given_parameters[parameter]
            else:
                # unknown parameter
                raise RuntimeError('Unknown parameter, ' + str(parameter) +
                                   ' can\'t be set')


class Carnivore(Fauna):
    parameters = {'eta': 0.125, 'F': 10.0, 'beta': 0.75, 'w_birth': 6.0,
                  'sigma_birth': 1.0, 'phi_age': 0.4, 'phi_weight': 0.4,
                  'a_half': 60, 'w_half': 4.0, 'gamma': 0.8, 'zeta': 3.5,
                  'xi': 1.1, 'mu': 0.4, 'DeltaPhiMax': 10.0, 'lambda': 1.0}

    def __init__(self, given_parameters=None):
        super().__init__(given_parameters)
        self._killing_probablity = 0
        if given_parameters is not None:
            # if we have given any subset of new parameters, we are going to
            # call that function that will overwrite the default parameters
            self.set_given_parameters(given_parameters)
            # and after that we set the new updated class variable to the attribute
        self.parameters = Carnivore.parameters
        self._weight = gauss(self.parameters['w_birth'],
                             self.parameters['sigma_birth'])

    @staticmethod
    def set_given_parameters(given_parameters):
        for parameter in given_parameters:
            if parameter in Herbivore.parameters:
                if parameter == 'eta' and given_parameters[parameter] > 1:
                    raise ValueError('Illegal parameter value, eta '
                                     'can\'t be more than 1')
                elif given_parameters[parameter] <= 0:
                    # protect against negative values
                    raise ValueError('Illegal parameter value, ' +
                                     str(parameter) + ' can\'t be zero or '
                                                      'negative')
                else:
                    #if given_parameters[parameter] >= 0
                    Carnivore.parameters[parameter] = \
                        given_parameters[parameter]
            else:
                # unknown parameter
                raise RuntimeError('Unknown parameter, ' + str(parameter) +
                                   ' can\'t be set')

    def calculate_killing_probablity(self, herbivore_fitness):
        if self.fitness <= herbivore_fitness:
            self.killing_probablity = 0
        elif 0 < self.fitness - herbivore_fitness < self.parameters[
            'DeltaPhiMax']:
            self.killing_probablity = (self.fitness - herbivore_fitness) / \
                                      self.parameters['DeltaPhiMax']
        else:
            self.killing_probablity = 1


if __name__ == '__main__':
    from random import seed
    new_params = {'eta': 0.1}
    h = Herbivore(new_params)
    f = Fauna()
    c = Carnivore(new_params)
    print(h)
    print(h.parameters)
    print(h.age)
    print(h.weight)
    print(c.weight)
    print(c.parameters)
    print(c.weight)
    print(h.weight)
    c.grow_up()
    h.grow_up()
    print(c.weight)
    print(h.weight)
    c.grow_up()
    h.grow_up()
    print(c.weight)
    print(h.weight)
    #print(f.parameters)
