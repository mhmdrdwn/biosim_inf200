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
from decimal import *

from biosim.simulation import BioSim
from biosim.fauna import Fauna
from biosim.fauna import Herbivore
from biosim.fauna import Carnivore
from biosim.landscapes import Jungle
from random import seed
from random import gauss


class TestFauna:
    def test_age(self):
        c = Carnivore()
        h = Herbivore()
        assert c.age == 0
        assert h.age == 0
        h.grow_up()
        assert h.age == 1
        assert c.age == 0
        c.grow_up()
        c.grow_up()
        assert h.age == 1
        assert c.age == 2
        # age increases one year after one year

    def test_weight(self):
        # basic random test, we need advanced tests
        c_params = {'w_birth': 4.0, 'sigma_birth': 1.7}
        h_params = {'w_birth': 2.0, 'sigma_birth': 1.5}
        seed(1)
        c = Carnivore(c_params)
        seed(1)
        h = Herbivore(h_params)
        assert c.weight == 6.189914080364287
        assert h.weight == 3.9322771297331944
        # initial weight should be a function that is decorated as variable
        # it's following Gaussain distro, the seed 1 will generate that value

    def test_grow_up(self):
        seed(1)
        h_params = {'eta': 0.30, 'w_birth': 2.0, 'sigma_birth': 1.5}
        h = Herbivore(h_params)
        seed(1)
        c_params = {'eta': 0.30, 'w_birth': 4.0, 'sigma_birth': 1.7}
        c = Carnivore(c_params)
        c_weight_before_grow = c.weight
        h_weight_before_grow = h.weight
        c.grow_up()
        h.grow_up()
        c_weight_after_grow = c.weight
        h_weight_after_grow = h.weight
        assert c_weight_before_grow - c_weight_after_grow == pytest.approx(1.856974224109286)
        assert h_weight_before_grow - h_weight_after_grow == pytest.approx(1.1796831389199582)
        # weight weight by eta factor every year

    def test_fitness(self):
        seed(1)
        h_params = {'phi_age': 0.3, 'phi_weight': 0.5, 'a_half': 40, 'w_half': 10}
        h = Herbivore(h_params)
        seed(1)
        c_params = {'phi_age': 0.4, 'phi_weight': 0.6, 'a_half': 60, 'w_half': 10}
        c = Carnivore(c_params)
        assert c.fitness == pytest.approx(0.09228477266076363)
        assert 0 <= c.fitness <= 1
        c.weight = 0
        assert c.fitness == 0
        c.weight = 0
        assert h.fitness == pytest.approx(0.04591907551573919)
        assert 0 <= h.fitness <= 1
        h.weight = 0
        assert h.fitness == 0

    def test_move_probability(self):
        seed(1)
        h_params = {'mu': 0.3, 'phi_age': 0.3, 'phi_weight': 0.5, 'a_half': 40, 'w_half': 10}
        h = Herbivore(h_params)
        seed(1)
        c_params = {'mu': 0.25, 'phi_age': 0.4, 'phi_weight': 0.6, 'a_half': 60, 'w_half': 10}
        c = Carnivore(c_params)
        assert c.move_probability == pytest.approx(0.023071193165190906)
        assert h.move_probability == pytest.approx(0.013775722654721757)

    def test_birth_probability(self):
        seed(1)
        h_params = {'gamma': 0.7, 'phi_age': 0.3, 'phi_weight': 0.5, 'a_half': 40, 'w_half': 10, 'zeta': 1}
        h = Herbivore(h_params)
        seed(1)
        c_params = {'gamma': 0.6, 'phi_age': 0.4, 'phi_weight': 0.6, 'a_half': 60, 'w_half': 10, 'zeta': 1}
        c = Carnivore(c_params)
        assert c.birth_probablity(1) == 0
        assert h.birth_probablity(1) == 0
        # probablity is zero if animals is less than 2
        # probablity should be more than 0 if animals >= 2
        # probablity of giving birth if there are two animals in the cell
        assert c.birth_probablity(2) == pytest.approx(0.055370863596458174)
        assert h.birth_probablity(2) == pytest.approx(0.03214335286101743)
        # probability should be 0 if the weight is less than
        # zeta(w_birth+sigma_birth)
        h.parameters['zeta'] = 5
        c.parameters['zeta'] = 4
        assert c.birth_probablity(2) == 0
        assert h.birth_probablity(2) == 0

    def test_death(self):
        h = Herbivore()
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
        assert h.weight == pre_weight + h.beta * h.F
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
        assert c.kill_probablity == (c.fitness - h.fitness) / DeltaPhiMax
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
        assert h.weight == pre_weight + h.beta * h.F
        # when the animals eats F animals, it will have a new weight beta*F
