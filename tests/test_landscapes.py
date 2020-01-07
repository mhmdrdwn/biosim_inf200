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

