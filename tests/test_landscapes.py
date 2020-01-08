# -*- coding: utf-8 -*-

"""
Test set for landscapes class functionality and attributes.

This set of tests checks the landscapes classes methods perform as expected as per
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
from biosim.landscapes import Desert
from biosim.landscapes import Ocean
from biosim.landscapes import Mountains
from biosim.landscapes import Savannah
from biosim.landscapes import Jungle
from biosim.fauna import Herbivores
from biosim.fauna import Carnivores

""" is it possible now to import just biosim.landscapes as landscapes
since it's not conflicting with anything here"""


class TestLandscapes:
    def test_geogr_map(self):
        pass
        # the sea is surrounding the island, should it be here or
        # simulation class


class TestDesert:
    def test_no_fodder(self):
        """No fodder available in the desert"""
        d = Desert()
        assert d.fooder == 0


class TestOcean:
    def test_nu_animals(self):
        o = Ocean()
        assert o.nu_animals == 0


class TestMountains:
    def test_nu_animals(self):
        m = Mountains()
        assert m.nu_animals == 0


class TestSavannah:
    def test_yearly_growth(self):
        s = Savannah()
        assert s.fodder == s.f_max
        h = Herbivores()
        h.eat()
        assert 0 <= s.fodder < s.f_max
        assert s.fodder == s.f_max - h.F
        # the initial amount is f_max
        s.apply_yearly_growth()
        post_f = s.fodder
        assert post_f >= s.fooder
        #assert post_f - pre_f == s.alpha*(s.f_max - pre_f)
        # the growth or the difference between them is given by the fomula


class TestJungle:
    def test_yearly_growth(self):
        j = Jungle()
        assert j.fodder == j.f_max
        h = Herbivores()
        assert j.fodder <= j.f_max
        #assert j.fodder == j.f_max - j.nu_herbivores*h.F
        j.apply_yearly_growth()
        assert j.fodder == j.f_max
        # at the start of eac simulation the fodder will have f_max
        # after a year the fodder will have f_max, no matter how much was eaten
        # still not right

