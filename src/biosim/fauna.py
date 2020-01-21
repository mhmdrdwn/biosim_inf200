# -*- coding: utf-8 -*-

"""
Fauna Classes and subclasses (Herbivore, Carnivore).
Fauna class is a base class, all objects are instantiated from the
Carnivore and Herbivore subclasses

"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from abc import ABC, abstractmethod
import numpy as np
import math


class Fauna(ABC):
    """
    Animal abstract superclass, inheriting from the (Abstract Base class) ABC,
    it has two subclasses which are animal species.
    Herbivores & Carnivores. The two subclasses feed in different ways.
    """
    parameters = {}

    @abstractmethod
    def __init__(self, age=None, weight=None):

        """
        Constructor for superclass, if age or weight is initialised
        automatically if not provided. Also, specifing invalid age or weight
         values will raise a a value error. Initial fitness is
        set to zero.

        Parameters
        ----------
        age: int
        weight: float, int

        """
        if age is None:
            self.age = 0
        else:
            self.raise_non_valid_attribute('Age', age)
            self.age = age

        if weight is None:
            self._weight = self.set_default_weight()
        else:
            self.raise_non_valid_attribute('Weight', weight)
            self._weight = weight

        self.just_give_birth = False

        self._fitness = None
        self.calculate_fitness()
        self._recompute_fitness = False

    @property
    def weight(self):
        return self._weight

    @staticmethod
    def raise_non_valid_attribute(attribute_name, attribute):
        """
        Raise an error if the input is invalid type

        Parameters
        ----------
        attribute_name : str
        attribute : value of the attribute. i.e. int

        """
        if not isinstance(attribute, (int, float)):
            raise ValueError(attribute_name + ' of animal can\'t be set to '
                             + attribute_name +
                             ', it has to be integer or float')

    @classmethod
    def set_default_weight(cls):
        """
        Sets default value for class attributes - age & weight of animal.
        Birth weight draws from gaussian distribution.

        Parameters
        ----------
        attribute_name: str

        """
        return np.random.normal(cls.parameters['w_birth'],
                                cls.parameters['sigma_birth'])

    def grow_up(self):
        """
        Increase age yearly

        """
        self.age += 1

    def lose_weight(self):
        """
        Decreases weight of the animal every year by the factor 'eta'
        """
        weight_to_reduce = self.weight * self.parameters['eta']
        self._weight -= weight_to_reduce
        self._recompute_fitness = True

    @property
    def fitness(self):
        """
        Getter with a flag variable reset to True when the fitness is
        recalculated using the equation.
        Returns
        -------
        fitness : float

        """
        if self._recompute_fitness:
            self.calculate_fitness()
            self._recompute_fitness = False
        return self._fitness

    @staticmethod
    def fitness_formula(age, weight, parameters):
        """
        Computes fitness according to the formula:
        Phi = q(-1, a, a_half, phi_age)*q(+1, w, w_half, phi_weight)
        and always and always 0=< phi =< 1

        Parameters
        ----------
        age: int
        weight: float
        parameters: keys from the class dictionary parameters

        Returns
        -------
        q1*q2: float
            Which is equal to fitness.

        """
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
        if self.weight == 0:
            self._fitness = 0
        else:
            self._fitness = self.fitness_formula(
                self.age, self.weight, self.parameters)

    @property
    def move_prob(self):
        """
        probability of animal to move from cell to another

        Returns
        -------
        animal movement probability: boolean

        """
        move_probability = self.parameters['mu'] * self._fitness
        return move_probability > np.random.random()

    def birth_prob(self, num_fauna):
        """
        Calculates the probability to give birth as follows:
        gamma * fitness * (number of fauna-1)
        If this equation is greater than one, the probability is one.
        The probability is zero in one of below conditions occur:
        - if there is less than 2 animals of same kind
        - or the weight of animal is less than below equation:
          zeta * (w_birth + sigma_birth)

        Parameters
        ----------
        num_fauna: int

        Returns
        -------
        birth probability: bool

        """
        zeta = self.parameters['zeta']
        w_birth = self.parameters['w_birth']
        sigma_birth = self.parameters['sigma_birth']
        if num_fauna >= 2 and self.weight >= zeta * (w_birth + sigma_birth):
            gamma = self.parameters['gamma']
            return np.random.random() < min(1, gamma *
                                            self._fitness * (num_fauna - 1))
        else:
            return False

    def lose_weight_give_birth(self, baby):
        """
        Decreases mother animal weight 'xi' times of the actual birth weight of
        the baby.

        Parameters
        ----------
        baby: obj
            An object of any Fauna subclasses, either Carnivores or Herbivores
            based on mother's species
        """
        if self.weight >= baby.weight * baby.parameters['xi']:
            self._weight -= baby.weight * baby.parameters['xi']
            self.just_give_birth = True

    @property
    def death_prob(self):
        """
        Returns death probability according to the formula.
        The death probability of an animal with zero fitness is 1.

        Returns
        -------
        death probability: bool

        """
        if self._fitness == 0:
            return True
        else:
            return np.random.random() < self.parameters['omega'] \
                   * (1 - self._fitness)

    def eat(self, amount_to_eat):
        """
        Increases animal weight after receiving food

        Parameters
        ----------
        amount_to_eat: int, float

        """
        self._weight += self.parameters['beta'] * amount_to_eat

    @classmethod
    def set_given_parameters(cls, params):
        """
        save the user defined parameter value for Carnivore and Herbivore
        inside the class variables parameters.

        Parameters
        ----------
        params: dict

        """

        for parameter in params:
            if parameter in cls.parameters:
                if parameter == 'eta' and params['eta'] > 1:
                    raise ValueError('Illegal parameter value, eta '
                                     'can\'t be more than 1')
                if parameter == 'DeltaPhiMax' and params[parameter] <= 0:
                    raise ValueError('Illegal parameter value, ' +
                                     str(parameter) + ' can\'t be or negative')
                if params[parameter] < 0:
                    raise ValueError('Illegal parameter value, ' +
                                     str(parameter) + ' can\'t be negative')
                else:
                    cls.parameters[parameter] = params[parameter]
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
        subclass of Fauna class.

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
        subclass of Fauna class.

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
        - Carnivore only can kill the herbivore with less fitness than its own
          fitness. So that, if the fitness of carnivore is less than herbivore's
          the killing probability is zero.
        - If the difference between two animals (carnivore and herbivore)
          is more than the parameter 'DeltaPhiMax', killing probability is 100%.
        - In other cases, the killing probability is drawn by following formula:
          (carnivore fitness - herbivore fitness) / 'DeltaPhiMax'

        Parameters
        ----------
        herbivore_to_kill: obj
            An object of Herbivore class

        Returns
        -------
        _kill_prob: bool
        """

        if self._fitness <= herbivore_to_kill.fitness:
            self._kill_prob = 0
        elif 0 < self._fitness - herbivore_to_kill.fitness < \
                self.parameters['DeltaPhiMax']:
            self._kill_prob = (self._fitness - herbivore_to_kill.fitness) / \
                              self.parameters['DeltaPhiMax']
        else:
            self._kill_prob = 1
        return np.random.random() < self._kill_prob
