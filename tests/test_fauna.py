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
        f.grow()
        assert f.weight == f.eta*initial
        # weight increases by eta factor every year
        f.eat()
        assert f.weight == f.beta*initial
        # weight increases by beta factor when eating


class TestHerbivores:
    pass
