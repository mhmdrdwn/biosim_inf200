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
    all_fauna = []

    def __init__(self, island_map, init_pop):
        self.island_map = self.string_to_np_array(island_map)
        self.not_surrounded_by_ocean(self.island_map)
        Map.all_fauna.append(init_pop)
        # self.map = self.create_map(self.island_map)
        # self.all_fauna = all_fauna
        # Those animals are just initial for all cells, letr we need to add all_fauna
        h1 = Herbivore()
        h2 = Herbivore()
        c1 = Carnivore()
        c2 = Carnivore()
        animals = {'Herbivore': [h1, h2], 'Carnivore': [c1, c2]}
        self.landscape_cells = {'O': Ocean(),
                                'S': Savannah(animals),
                                'M': Mountain(),
                                'J': Jungle(animals),
                                'D': Desert(animals)}

    def create_cell(self, cell_letter):
        return self.landscape_cells[cell_letter]

    @staticmethod
    def matrix_dim(map):
        rows = map.shape[0]
        cols = map.shape[1]
        return rows, cols

    def edges(self, map):
        rows, cols = self.matrix_dim(map)
        map_edges = [map[0, :cols], map[rows - 1, :cols],
                     map[:rows - 1, 0], map[:rows - 1, cols - 1]]

        print(map_edges)
        print(len(map_edges))
        print()
        print(rows * cols)
        return map_edges

    def not_surrounded_by_ocean(self, map):
        # protect against non ocean edges
        edges = self.edges(map)
        for side in edges:
            if not np.all(side == 'O'):
                raise ValueError('The given geography string is not valid.'
                                 'The edges of geography has to be ocean')

    def create_map(self, map):
        char_map = self.string_to_np_array(map)
        # for element in geogr_array:
        landscape_array = np.empty(char_map.shape, dtype=object)
        # we did that to build array of the same dimesions
        for i in np.arange(char_map.shape[0]):
            for j in np.arange(char_map.shape[1]):
                # iterate through the given character array and build
                # object of landscapes for each character
                # we saved here the landscape class and instantiate the object
                cell_letter = char_map[i][j]
                landscape_array[i][j] = self.create_cell(cell_letter)
                # all object are saved inside the numpy array in output
                # animals list should be given as arguments to the
                # object of landscape
        return landscape_array

    def string_to_np_array(self, map):
        map_string_clean = map.replace(' ', '')
        char_map = np.array(
            [[j for j in i] for i in map_string_clean.splitlines()])
        # convert string to numpy array with the same diemsions
        return char_map

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

    def migrate(self, current_cell, map, x, y):
        for species in current_cell.in_cell_fauna:
            for animal in species:
                if np.random.random() > animal.move_prob:
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

    def add_animals_population(self, population):
        print(population)

    def annual_cycle(self):
        rows = self.map.shape[0]
        cols = self.map.shape[1]
        for x in range(0, rows):
            for y in range(0, cols):
                cell = self.map[x, y]
                cell.feed_animals()
                # step 1 feeding
                cell.migrate(cell, map, x, y)
                # step 2 migrate
                cell.grow_up_animals()
                # step 4, grow_up
                cell.lose_weight_animals()
                cell.die_animals()

