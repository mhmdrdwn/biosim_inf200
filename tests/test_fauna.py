# -*- coding: utf-8 -*-

"""
Test set for Animals class functionality.

This set of tests checks the Animals class methods perform as expected as per
the provided modeling.

"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'


import pytest
import pandas
import glob
import os
import os.path

from biosim.simulation import BioSim
from biosim.fauna import Fauna
from biosim.fauna import Herbivores
from biosim.fauna import Carnivores
from biosim.landscapes import Jungle
from random import seed
from random import gauss


class TestFauna:
    def test_age(self):
        """No fodder available in the desert"""
        f = Fauna()
        assert f.age == 0
        f.grow()
        assert f.age == 1
        f.grow()
        assert f.age == 2
        # age increases one year after one year

    def test_weight(self):
        f = Fauna()
        initial = f.weight
        seed(1)
        assert f.weight == 1.2881847531554629
        # initial weight should be a function that is decorated as variable
        # it's following Gaussain distro, the seed 1 will generate that value
        f.grow()
        assert f.weight == f.eta*initial
        # weight increases by eta factor every year
        f.eat()
        assert f.weight == f.beta*initial
        # weight increases by beta factor when eating
        # how to test gaussian distribution of weights?

    def test_fitness(self):
        f = Fauna()
        f.phi_weight = 0.1
        f.phi_age = 0.2
        f.a_half = 40
        # how can we get weight from gaussain ditribution
        assert f.fitness == 0.1630552263
        assert 0 <= f.fitness <= 1


    def test_migration(self):
        f = Fauna()
        f.migrate()


    def test_birth(self):
        f = Fauna()
        f.fitness = 0.1630552263
        f.gamma = 0.2
        j = Jungle()
        j.nu_animals = 1
        assert f.birth == 0
        # probablity is zero if animals is less than 2
        j.nu_animals = 2
        assert f.birth > 0
        # probablity should be more than 0
        assert f.birth == 0.03261104526
        # probablity of giving birth if there are two animals in the cell
        f.weight  = 33.00
        assert f.birth == 0
        # probablity is zero when weight is less than 33.25
        # we need to test weights at the birth

    def test_death(self):
        h = Herbivores()
        h.fitness = 0
        assert h.death() == 0
        h.fitness = 0.1
        assert h.death() > 0
        assert h.death == 0.36
        # probablity of death given fitness 0.1 will be 0.36
    

class TestHerbivores:
    def test_herbivores_weight(self):
        h = Herbivores()
        pre_weight = h.weight
        h.beta = 0.9
        h.F = 10
        h.eat()
        assert h.weight == pre_weight + h.beta*h.F
        # when the animals eats F fodder, it will have anew weight beta*F


class TestCarnivores:
    def test_kill_probability(self):
        c = Carnivores()
        h = Herbivores()
        c.fitness = 0.4
        h.fitness = 0.5
        assert c.kill_probablity == 0
        c.fitness = 0.5
        h.fitness = 0.4
        DeltaPhiMax = 10.0
        assert c.kill_probablity == (c.fitness - h.fitness)/DeltaPhiMax
        assert c.kill_probablity == 0.01
        # kill probablity should follow the rules given in carinvores based on
        # the fitness of herbi and carni
        c.fitness = 20
        h.fitness = 9
        assert c.kill_probablity == 1

    def test_carinvories_weight(self):
        c = Carnivores()
        h = Herbivores()
        pre_weight = h.weight
        h.beta = 0.75
        h.F = 50
        h.eat()
        assert h.weight == pre_weight + h.beta*h.F
        # when the animals eats F animals, it will have a new weight beta*F

