# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from biosim.landscapes import *
import numpy as np
# that's wrong


class Map:
    def __init__(self, geogr_string, fauna_objects):
        self.geogr_string = geogr_string
        self.landscape_char_dict = {'O': Ocean, 'S': Savannah, 'M': Mountain,
                          'J': Jungle, 'D': Desert}
        self.fauna_objects = fauna_objects
        #self.landscape_array = np.array()

    def create_map_dict(self):
        given_geogr_array = self.string_to_np_array()
        # for element in geogr_array:
        landscape_array = np.empty(given_geogr_array.shape, dtype=object)
        # we did that to build array of the same dimesions
        for i in np.arange(given_geogr_array.shape[0]):
            for j in np.arange(given_geogr_array.shape[1]):
                # iterate through the given character array and build
                # object of landscapes for each character
                landscape_class = self.landscape_char_dict[given_geogr_array[i][j]]
                # we saved here the landscape class and instantiate the object
                landscape_array[i][j] = landscape_class(self.fauna_objects)
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

    def migrate(self):
        map = self.create_map_dict()
        rows = map.shape[0]
        cols = map.shape[1]
        for x in range(0, rows):
            for y in range(0, cols):
                current_cell = map[x, y]
                for animal in current_cell.fauna_objects_dict:
                    if np.random.random() > animal.move_probability:
                        adj_cells = [map[x-1, y], map[x+1, y], map[x, y-1], map[x, y+1]]
                        cell_probabilities_list = [current_cell.probability_to_which_cell(
                            animal, cell, adj_cells) for cell in adj_cells]
                        # get the adjacent cells for all the current cells and calculate the relevant abundance of fodder
                        #relative_fodder_abundance =[i.propensity() for i in adj_cells]
                        #the cell with relevant abundance of fodder will make the animal move to it
                        maximum_probability_index =  cell_probabilities_list.index(max(cell_probabilities_list))
                        cell_with_maximum_probability = adj_cells[maximum_probability_index]
                        #then remove animal from the current cell and add it to the distination cell

                        current_cell.remove_fauna()
                        cell_with_maximum_probability.add_fauna()


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

h1 = Herbivore()
h1.fitness = 10
h2 = Herbivore()
h2.fitness = 20
c1 = Carnivore()
c1.fitness = 10
c2 = Carnivore()
c2.fitness = 20
animals = {'Carnivore': [c1, c2], 'Herbivore': [h1, h2]}

m = Map(map_str, animals)
print(m.geogr_string)
#print(m.char_dict)
#print(m.create_map_dict())
#print(m.string_to_np_array())
print(m.migrate())