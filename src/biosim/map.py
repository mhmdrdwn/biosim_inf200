# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from biosim.landscapes import Desert, Ocean, Mountain, Savannah, Jungle
from biosim.fauna import Herbivore, Carnivore
import numpy as np


class Map:

    def __init__(self, island_map):
        self.island_map = self.string_to_np_array(island_map)
        self._cells_dims = None
        self.not_surrounded_by_ocean(self.island_map)
        self.landscape_classes = {'O': Ocean,
                                  'S': Savannah,
                                  'M': Mountain,
                                  'J': Jungle,
                                  'D': Desert}
        self._fauna_classes = {'Carnivore': Carnivore,
                                'Herbivore': Herbivore}

        self._cells = self.create_map_of_landscape_objects()


    @property
    def cells(self):
        """Returns full data matrix."""
        return self._cells

    def mean_value(self):
        """Returns mean value of system elements."""
        pass

    def create_cell(self, cell_letter):
        return self.landscape_classes[cell_letter]()

    @property
    def cells_dims(self):
        rows = self._cells.shape[0]
        cols = self._cells.shape[1]
        return rows, cols

    def edges(self, map_array):
        rows, cols = map_array.shape[0], map_array.shape[1]
        map_edges = [map_array[0, :cols], map_array[rows - 1, :cols],
                     map_array[:rows - 1, 0], map_array[:rows - 1, cols - 1]]
        return map_edges

    def not_surrounded_by_ocean(self, map_array):
        # protect against non ocean edges
        edges = self.edges(map_array)
        for side in edges:
            if not np.all(side == 'O'):
                raise ValueError('The given geography string is not valid.'
                                 'The edges of geography has to be ocean')

    def create_map_of_landscape_objects(self):
        # for element in geogr_array:
        cells_array = np.empty(self.island_map.shape, dtype=object)
        # we did that to build array of the same dimesions
        for i in np.arange(self.island_map.shape[0]):
            for j in np.arange(self.island_map.shape[1]):
                # iterate through the given character array and build
                # object of landscapes for each character
                # we saved here the landscape class and instantiate the object
                cell_letter = self.island_map[i][j]
                cells_array[i][j] = self.create_cell(cell_letter)
                # all object are saved inside the numpy array in output
                # animals list should be given as arguments to the
                # object of landscape
        return cells_array

    @staticmethod
    def string_to_np_array(map_str):
        map_string_clean = map_str.replace(' ', '')
        char_map = np.array(
            [[j for j in i] for i in map_string_clean.splitlines()])
        # convert string to numpy array with the same diemsions
        return char_map

    def adj_cells(self, x, y):
        rows, cols = self.cells_dims
        adj_cells_list = []
        if x > 0:
            adj_cells_list.append(self._cells[x - 1, y])
        if x + 1 < rows:
            adj_cells_list.append(self._cells[x + 1, y])
        if y > 0:
            adj_cells_list.append(self._cells[x, y - 1])
        if y + 1 < cols:
            adj_cells_list.append(self._cells[x, y + 1])
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

    def add_animals(self, pop):
        for animal_group in pop:
            loc = animal_group['loc']
            animals = animal_group['pop']
            for animal in animals:
                species = animal['species']
                age = animal['age']
                weight = animal['weight']
                species_class = self._fauna_classes[species]
                animal_object = species_class(age=age, weight=weight)
                cell = self._cells[loc]
                cell.add_animal(animal_object)

    def total_num_animals_per_species(self, species):
        num_animals = 0
        rows, cols = self.cells_dims
        for x in range(0, rows):
            for y in range(0, cols):
                cell = self._cells[x, y]
                num_animals += len(cell._in_cell_fauna[species])
        return num_animals

    def run_stage_of_cycle(self, stage_method):
        rows, cols = self.cells_dims
        for x in range(0, rows):
            for y in range(0, cols):
                cell = self._cells[x, y]
                stage_method_call = cell.globals()[stage_method]
                stage_method_call()

    def update(self):
        cycle_stage_methods = ['feed_animals', 'give_birth_animals',
                               'migrate_animals', 'grow_up_animals',
                               'lose_weight_animals', 'die_animals']
        for stage in cycle_stage_methods:
            self.run_stage_of_cycle(stage)

    # not needed methods
    def give_birth_all_cells(self):
        cols, rows = self.cells_dims
        for x in rows:
            for y in cols:
                cell = self._cells[x, y]
                cell.give_birth_animals()
    # same can be done for all methjods here, to run for all cells
