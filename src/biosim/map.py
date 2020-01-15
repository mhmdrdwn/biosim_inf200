# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from biosim.fauna import Herbivore, Carnivore
from biosim.landscapes import Desert, Ocean, Mountain, Savannah, Jungle
import numpy as np


# that's wrong


class Map:
    def __init__(self, geogr_string, all_fauna):
        self.geogr_string = geogr_string
        self.all_fauna = all_fauna

    def create_cell(self, cell_letter):
        # Those animals are just initial for all cells, letr we need to add all_fauna
        h1 = Herbivore()
        h2 = Herbivore()
        c1 = Carnivore()
        c2 = Carnivore()
        animals = {'Herbivore': [h1, h2], 'Carnivore': [c1, c2]}
        landscape_cells = {'O': Ocean(),
                           'S': Savannah(animals),
                           'M': Mountain(),
                           'J': Jungle(animals),
                           'D': Desert(animals)}
        return landscape_cells[cell_letter]

    def create_map(self):
        given_geogr_array = self.string_to_np_array()
        # for element in geogr_array:
        landscape_array = np.empty(given_geogr_array.shape, dtype=object)
        # we did that to build array of the same dimesions
        for i in np.arange(given_geogr_array.shape[0]):
            for j in np.arange(given_geogr_array.shape[1]):
                # iterate through the given character array and build
                # object of landscapes for each character
                # we saved here the landscape class and instantiate the object
                cell_letter = given_geogr_array[i][j]
                landscape_array[i][j] = self.create_cell(cell_letter)
                # all object are saved inside the numpy array in output
                # animals list should be given as arguments to the
                # object of landscape
        return landscape_array

    def string_to_np_array(self):
        geogr_string_clean = self.geogr_string.replace(' ', '')
        char_array = np.array([[j for j in i] for i in geogr_string_clean.splitlines()])
        # convert string to numpy array with the same diemsions
        return char_array

    @staticmethod
    def adj_cells(map, x, y):
        rows = map.shape[0]
        cols = map.shape[1]
        adj_cells_list = []
        if x > 0:
            adj_cells_list.append(map[x - 1, y])
        if x + 1 < rows:
            adj_cells_list.append(map[x + 1, y])
        if y > 0:
            adj_cells_list.append(map[x, y - 1])
        if y + 1 < cols:
            adj_cells_list.append(map[x, y + 1])
        return adj_cells_list

    @staticmethod
    def total_adj_propensity(cells, animal):
        total_propensity = 0
        for cell in cells:
            total_propensity += cell.propensity(animal)
        return total_propensity

    def migrate(self):
        map = self.create_map()
        rows = map.shape[0]
        cols = map.shape[1]
        for x in range(0, rows):
            for y in range(0, cols):
                current_cell = map[x, y]
                self.move_animals(current_cell, map, x, y)

    def move_animals(self, current_cell, map, x, y):
        for species in current_cell.in_cell_fauna:
            for animal in species:
                if np.random.random() > animal.move_probability:
                    adj_cells_list = self.adj_cells(map, x, y)
                    cell_probabilities_list = [cell.probability_of_cell(animal)
                                               for cell in adj_cells_list]
                    # get the adjacent cells for all the current cells and calculate the relevant abundance of fodder
                    # relative_fodder_abundance =[i.propensity() for i in adj_cells]
                    # the cell with relevant abundance of fodder will make the animal move to it
                    maximum_probability_index = cell_probabilities_list.index(
                        max(cell_probabilities_list))
                    cell_with_maximum_probability = adj_cells_list[
                        maximum_probability_index]
                    # then remove animal from the current cell and add it to the distination cell
                    current_cell.remove_fauna(animal)
                    cell_with_maximum_probability.add_fauna(animal)
