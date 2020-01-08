# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'


class Fauna:
    def __init__(self):
        self.parameters = {'carni': {'eta': 0.125, 'F': 10.0, 'beta': 0.75},
                           'herbi': {'eta': 0.05, 'F': 50.0, 'beta': 0.9}}
        # parameters dictionary, stil need a better implimentation of it
        self.age = 0
        # initial age is zero
        self.weight = 1
        # how to do that ????? Normal distribution of weights (what weights??)

    def grow_up(self):
        self.age += 1
        # age increase by 1 each year

    def decrease_weight_annual(self):
        self.weight += self.weight*self.parameters['carni']['eta']
        # that's just for carni, still need to code herbi

    def eat(self):
        self.weight += self.parameters['carni']['beta']*self.parameters['carni']['F']
        # that's just for carni, still need to code herbi


class Herbivores(Fauna):
    pass


class Carnivores(Fauna):
    pass


f = Fauna()
print(f.weight)
f.eat()
print(f.weight)
aaaa