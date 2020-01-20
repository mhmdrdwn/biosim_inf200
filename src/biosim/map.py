# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from biosim.landscapes import Landscape, Desert, Ocean, Mountain, Savannah, Jungle
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
                num_animals += len(cell.in_cell_fauna[species])
        return num_animals

    def life_cycle(self):
        print('year')
        self.feed_stage()
        self.give_birth_stage()
        self.migrate_stage()
        self.grow_up_stage()
        self.lose_weight_stage()
        self.die_stage()

    def feed_stage(self):
        for [x, y], cell in np.ndenumerate(self._cells):
            cell.feed_animals()

    def give_birth_stage(self):
        for [x, y], cell in np.ndenumerate(self._cells):
            cell.give_birth_animals()

    def grow_up_stage(self):
        for [x, y], cell in np.ndenumerate(self._cells):
            cell.grow_up_animals()

    def lose_weight_stage(self):
        for [x, y], cell in np.ndenumerate(self._cells):
            cell.lose_weight_animals()

    def die_stage(self):
        for [x, y], cell in np.ndenumerate(self._cells):
            cell.die_animals()

    def migrate_stage(self):
        for [x, y], cell in np.ndenumerate(self._cells):
            cell.migrate(self.adj_cells(x, y))


if __name__ == '__main__':
    dict_={'a':1,"b":2}
    for i, j in dict_.items():
        print(i)
        print(j)
    a = {'ca':[1,2,3,4,5,6],'h':[0,9,8,6,7]}
    for i, j in a.items():
        for k in j:
            print(i)
            print(k)