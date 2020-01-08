# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'


class Landscapes:
    def __init__(self, geography_string):
        self.geography_string = geography_string
        self.available_fodder = 0
        self.nu_fauna = 0


class Desert(Landscapes):
    def __init__(self):
        self._available_fodder = 0
        # That's becuase it's not changable, so it's private variable


class Mountains(Landscapes):
    def __init__(self):
        pass


class Ocean(Landscapes):
    def __init__(self):
        self.nu_fauna = 0


class Savannah(Landscapes):
    def __init__(self):
        pass


class Jungle(Landscapes):
    def __init__(self):
        pass