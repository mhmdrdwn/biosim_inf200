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
""" is it possible now to import just biosim.landscapes as landscapes
since it's not conflicting with anything here"""


class TestLandscapes:
    pass


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
        pre_f = s.fodder
        s.apply_yearly_growth()
        post_f = s.fodder
        pre_f != post_f
        post_f - pre_f == s.alpha*(s.f_max - pre_f)
        # the growth or the difference between them is given by the fomula

class TestJungle:
    pass

