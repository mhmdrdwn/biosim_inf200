# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from biosim.landscapes import *
import numpy as np


# that's wrong


class Map:
    def __init__(self, geogr_string):
        self.geogr_string = geogr_string
        self.objects_list = []
        self.char_dict = {'O': Ocean, 'S': Savannah, 'M': Mountain,
                          'J': Jungle, 'D': Desert}

    def create_map_dict(self):
        given_geogr_array = self.string_to_np_array()
        # for element in geogr_array:
        landscape_array = np.empty(given_geogr_array.shape, dtype=object)
        # we did that to build array of the same dimesions
        for i in np.arange(given_geogr_array.shape[0]):
            for j in np.arange(given_geogr_array.shape[1]):
                # iterate through the given character array and build
                # object of landscapes for each character
                landscape_class = self.char_dict[given_geogr_array[i][j]]
                # we saved here the landscape class and instantiate the object
                landscape_array[i][j] = landscape_class()
                # all object are saved inside the numpy array in output
                # animals list should be given as arguments to the
                # object of landscape
        return landscape_array

    def string_to_np_array(self):
        geogr_string_clean = self.geogr_string.replace(' ', '')
        given_char_array = np.array([[j for j in i] for i in
                               geogr_string_clean.splitlines()])
        # convert string to numpy array with the same diemsions
        return given_char_array



map_str = """\
               OOOOOOOOOOOOOOOOOOOOO
               OOOOOOOOSMMMMJJJJJJJO
               OSSSSSJJJJMMJJJJJJJOO
               OSSSSSSSSSMMJJJJJJOOO
               OSSSSSJJJJJJJJJJJJOOO
               OSSSSSJJJDDJJJSJJJOOO
               OSSJJJJJDDDJJJSSSSOOO
               OOSSSSJJJDDJJJSOOOOOO
               OSSSJJJJJDDJJJJJJJOOO
               OSSSSJJJJDDJJJJOOOOOO
               OOSSSSJJJJJJJJOOOOOOO
               OOOSSSSJJJJJJJOOOOOOO
               OOOOOOOOOOOOOOOOOOOOO"""
m = Map(map_str)
print(m.geogr_string)
print(m.char_dict)
print(m.create_map_dict())
print(m.string_to_np_array())