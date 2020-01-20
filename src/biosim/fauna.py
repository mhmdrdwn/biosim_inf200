# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from abc import ABC, abstractmethod

from random import gauss
import math


class Fauna(ABC):
    """
    Animal abstract class, it has two subclasses which are animal species:
    Herbivores & Carnivores. They have certain characteristics in common, but
    feed in different ways.
    """
    parameters = {}

    @abstractmethod
    def __init__(self, age=None, weight=None):
        """

        """

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
        """
        Sets default value for class attributes - age & weight of animal.
        Birth weight draws from gaussian distribution.

        Parameters
        ----------
        attribute_name: str
        """
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
        """
        Increases animal age yearly
        """
        self.age += 1
        # age increase by 1 each year
        # decrease the weight by the factor eta

    def lose_weight(self):
        """
        Decreases weight of the animal every year.
        """
        weight_to_reduce = self._weight * self.parameters['eta']
        self._weight -= weight_to_reduce

    @property
    def fitness(self):
        # question why we have this ?

        self.calculate_fitness()
        return self._fitness

    @staticmethod
    def fitness_formula(age, weight, parameters):
        """
        Computes fitness according to the formula:
        Phi = q(-1, a, a_half, phi_age)*q(+1, w, w_half, phi_weight)

        Parameters
        ----------
        age: int
        weight: float
        parameters: keys from the class dictionary parameters

        Returns
        -------
        fitness: float
            Always between or equal to 0 and 1
        """
        # fitness formula
        q1 = 1 / (1 + math.exp((parameters['phi_age'])
                               * (age - parameters['a_half'])))
        q2 = 1 / (1 + math.exp((-1 * (parameters['phi_weight'])
                                * (weight - parameters['w_half']))))
        return q1 * q2

    def calculate_fitness(self):
        """
        Controls condition when weight is zero. Otherwise, calculate animal
        fitness which is based on age & weight of the animal.
        """
        # question why if age = 0 isn't checked?
        if self._weight == 0:
            self._fitness = 0
        else:
            self._fitness = self.fitness_formula(
                self.age, self._weight, self.parameters)

    @property
    def move_prob(self):
        """
        Returns the probability of animal movement which is a float number.
        """
        return self.parameters['mu'] * self.fitness
        # animal move probablity based on the equation

    def birth_prob(self, num_fauna):
        """
        Calculates the probability to give birth to an offspring is as follows:
        'gamma' * fitness * (number of fauna-1)
        If this equation is greater than one, the probability is one.
        The probability is zero if there is less than 2 animals of
        same kind or the weight of animal is less than below equation:
        zeta * (w_birth + sigma_birth)

        Parameters
        ----------
        num_fauna: int

        Returns
        -------
        birth probability: float

        """
        zeta = self.parameters['zeta']
        w_birth = self.parameters['w_birth']
        sigma_birth = self.parameters['sigma_birth']
        if num_fauna >= 2 and self.weight >= zeta * (w_birth + sigma_birth):
            gamma = self.parameters['gamma']
            return min(1, gamma * self.fitness * (num_fauna - 1))
        else:
            return 0

    def give_birth(self, baby):
        """
        Decreases mother animal weight 'xi' times of the actual birth weight
        of the baby.

        Parameters
        ----------
        baby: obj?
            An object of any Fauna subclasses, either Carnivores or Herbivores

        Returns
        -------
        weight: float
            Mother's weight after giving birth to an offspring
        """
        self._weight -= baby.weight * baby.parameters['xi']

    @property
    def death_prob(self):
        """
        Returns death probability according to the formula.
        The death probability of an animal with zero fitness is 1

        Returns
        -------
        death probability: float
        """
        if self.fitness == 0:
            return 1
        else:
            return self.parameters['omega'] * (1 - self.fitness)

    def eat(self, amount_to_eat):
        """
        Increases animal weight after receiving food.

        Parameters
        ----------
        amount_to_eat: ? (float or int)
        """
        self._weight += self.parameters['beta'] * amount_to_eat
        # the same behaviour for both carni and herbi, just the difference
        # is in the amount to eat

    @classmethod
    def set_given_parameters(cls, params):
        """
        Checks the user defined parameter value.

        Parameters
        ----------
        params: dict
        """

        for parameter in params:
            if parameter in cls.parameters:
                if parameter == 'eta' and params[parameter] > 1:
                    raise ValueError('Illegal parameter value, eta '
                                     'can\'t be more than 1')
                if parameter == 'DeltaPhiMax' and params[parameter] < 0:
                    raise ValueError('Illegal parameter value, ' +
                                     str(parameter) + ' can\'t be or negative')
                if params[parameter] <= 0:
                    # protect against negative values
                    raise ValueError('Illegal parameter value, ' +
                                     str(parameter) + ' can\'t be zero '
                                                      'or negative')
                else:
                    # if given_parameters[parameter] >= 0
                    cls.parameters[parameter] = \
                        params[parameter]
            else:
                raise RuntimeError('Unknown parameter, ' + str(parameter) +
                                   ' can\'t be set')


class Herbivore(Fauna):
    parameters = {'eta': 0.05, 'F': 10.0, 'beta': 0.9, 'w_birth': 8.0,
                  'sigma_birth': 1.5, 'phi_age': 0.2, 'phi_weight': 0.1,
                  'a_half': 40, 'w_half': 10.0, 'gamma': 0.8, 'zeta': 3.5,
                  'xi': 1.2, 'mu': 0.25, 'lambda': 1.0, 'omega': 0.4}

    def __init__(self, age=None, weight=None):
        """
        The constructor for the Herbivore class, which is a subclass of
        Fauna class.

        Parameters
        ----------
        age: int
        weight: float
        """
        super().__init__(age, weight)
        self.parameters = Herbivore.parameters


class Carnivore(Fauna):
    parameters = {'eta': 0.125, 'F': 50.0, 'beta': 0.75, 'w_birth': 6.0,
                  'sigma_birth': 1.0, 'phi_age': 0.4, 'phi_weight': 0.4,
                  'a_half': 60, 'w_half': 4.0, 'gamma': 0.8, 'zeta': 3.5,
                  'xi': 1.1, 'mu': 0.4, 'DeltaPhiMax': 10.0, 'lambda': 1.0,
                  'omega': 0.9}

    def __init__(self, age=None, weight=None):
        """
        The constructor for the Carnivore class, which is a subclass of
        Fauna class.

        Parameters
        ----------
        age: int
        weight: float
        """
        super().__init__(age, weight)
        self._kill_prob = None
        self.parameters = Carnivore.parameters

    def kill_prob(self, herbivore_to_kill):
        """
        Returns kill probability with following rules:
        Carnivore only can kill the herbivore with less fitness than its own
        fitness. So that, in this case, the killing probability is zero.
        Also, if the difference between two animals (carnivore and herbivore)
        is more than the parameter 'DeltaPhiMax', killing probability is 100%.
        In other cases, the killing probability is drawn by following formula:
        (carnivore fitness - herbivore fitness) / 'DeltaPhiMax'

        Parameters
        ----------
        herbivore_to_kill: obj?

        Returns
        -------
        _kill_prob: float
        """
        if self.fitness <= herbivore_to_kill.fitness:
            self._kill_prob = 0
        elif 0 < self.fitness - herbivore_to_kill.fitness < \
                self.parameters['DeltaPhiMax']:
            self._kill_prob = (self.fitness - herbivore_to_kill.fitness) / \
                              self.parameters['DeltaPhiMax']
        else:
            self._kill_prob = 1
        return self._kill_prob


if __name__ == '__main__':
    c1 = Carnivore()
    print(c1.parameters['F'])
    c1.set_given_parameters({'F': 40000})
    c2 = Carnivore()
    print(c1.parameters['F'])
    print(c2.parameters['F'])
    f = Fauna()
