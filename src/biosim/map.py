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
        for character in self.geogr_string:
            # build object of landscapes for each character
            if character in self.char_dict.keys():
                self.objects_list.append(self.char_dict[character]())
        print(len(self.objects_list))

    def string_to_np_array(self):
        geogr_string_clean = self.geogr_string.replace(' ', '')
        char_array = np.array([[j for j in i] for i in
                               geogr_string_clean.splitlines()])
        print(char_array)
        print(np.shape(char_array))


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
print(m.objects_list)
print(m.string_to_np_array())
