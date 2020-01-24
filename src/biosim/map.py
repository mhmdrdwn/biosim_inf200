# -*- coding: utf-8 -*-

"""
The map class contains map class. It has large scale methods like
- migration for all cells
- growing up all animals in all cells
- removing (die) animals in all cells
- giving birth in all cells
- feeding in all cells
- lose weights for all animals in all cells
and it has the life cycle for each year
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from .landscapes import Desert, Ocean, Mountain, Savannah, Jungle
from .fauna import Herbivore, Carnivore
import numpy as np


class Map:

    def __init__(self, island_map):
        """
        The constructor for Map class.
        Parameters
        ----------
        island_map: str
        """

        self._map = island_map
        self._island_map = self._string_to_np_array()
        self._not_surrounded_by_ocean(self._island_map)
        self._landscape_classes = {'O': Ocean,
                                  'S': Savannah,
                                  'M': Mountain,
                                  'J': Jungle,
                                  'D': Desert}
        self._fauna_classes = {'Carnivore': Carnivore,
                               'Herbivore': Herbivore}

        self._cells = self.create_map_of_landscape_objects()
        rows = self._cells.shape[0]
        cols = self._cells.shape[1]
        self.cells_dims = rows, cols

    @property
    def cells(self):
        """
        Returns full data matrix.
        Returns
        -------
        _cells: matrix
        """
        return self._cells

    def _create_cell(self, cell_letter):
        """
        create cell object based on given string
        Parameters
        ----------
        cell_letter: str
        Returns
        -------
        class of landscape (Jungle, Mountain, Savannah, Ocean, Desert)
        """
        return self._landscape_classes[cell_letter]()

    @staticmethod
    def _edges(map_array):
        """
        get the border element of the matrix, the cells on the border of the
         provided map array
        Parameters
        ----------
        map_array: array
        Returns
        -------
        map_edges: list
        """
        rows, cols = map_array.shape[0], map_array.shape[1]
        map_edges = [map_array[0, :cols], map_array[rows - 1, :cols],
                     map_array[:rows - 1, 0], map_array[:rows - 1, cols - 1]]
        return map_edges

    def _not_surrounded_by_ocean(self, map_array):
        """
        Raise an exception if the border of geography is not ocean
        Parameters
        ----------
        map_array: np.ndarray
        """
        edges = self._edges(map_array)
        for side in edges:
            if not np.all(side == 'O'):
                raise ValueError('The given geography string is not valid.'
                                 'The edges of geography has to be ocean')

    def create_map_of_landscape_objects(self):
        """
        Builds array of same dimension for elements in geogr_array. Then,
        iterate through the given character array and build the object of
        landscapes for each character. Afterwards, save the landscape class and
        instantiate the object.
        Returns
        -------
        cells_array: np.ndarray of landscape objects
        """
        cells_array = np.empty(self._island_map.shape, dtype=object)
        for i in np.arange(self._island_map.shape[0]):
            for j in np.arange(self._island_map.shape[1]):
                cell_letter = self._island_map[i][j]
                cells_array[i][j] = self._create_cell(cell_letter)
        return cells_array

    def _string_to_np_array(self):
        """
        Converts string to numpy array with the same diemsions.
        Returns
        -------
        char_map: np.ndarray
        """
        map_string_clean = self._map.replace(' ', '')
        char_map = np.array(
            [[j for j in i] for i in map_string_clean.splitlines()])
        return char_map

    def _adj_cells(self, x, y):
        """
        Returns the list of 4 adjacent cells.
        Parameters
        ----------
        x: int
        y: int
        Returns
        -------
        adj_cells_list: list
            List of 4 adjacent cells
        """
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
        """
        Add the given population to the animal population of the
        cell with specific location
        Parameters
        ----------
        pop: iterable
        """
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
        """
        Calculates number of animals per kind for all cells per species.
        Parameters
        ----------
        species: str
        Returns
        -------
        num_animals: dict
        """
        num_animals = 0
        rows, cols = self.cells_dims
        for x in range(0, rows):
            for y in range(0, cols):
                cell = self._cells[x, y]
                num_animals += len(cell.in_cell_fauna[species])
        return num_animals

    def life_cycle(self):
        """
        Calculates life cycle of animals yearly.
        """
        self._feed_stage()
        self._give_birth_stage()
        self._migrate_stage()
        self._grow_up_stage()
        self._lose_weight_stage()
        self._die_stage()

    def _feed_stage(self):
        """
        feeding all the animals in all cells
        """
        rows, cols = self.cells_dims
        for x in range(rows):
            for y in range(cols):
                self._cells[x, y].feed_animals()

    def _give_birth_stage(self):
        """
        giving birth all the animals in all cells, then adding newborn babies
        to the adult animals to be considered in procreatation next year and
        also to be considered in all life cycle stages.
        """
        rows, cols = self.cells_dims
        for x in range(rows):
            for y in range(cols):
                self._cells[x, y].give_birth_animals()

        for x in range(rows):
            for y in range(cols):
                self._cells[x, y].add_baby_to_adult_animals()

    def _grow_up_stage(self):
        """
        growing up all the animals in all cells
        """
        rows, cols = self.cells_dims
        for x in range(rows):
            for y in range(cols):
                self._cells[x, y].grow_up_animals()

    def _lose_weight_stage(self):
        """
        losing weight for all the animals in all cells
        """
        rows, cols = self.cells_dims
        for x in range(rows):
            for y in range(cols):
                self._cells[x, y].lose_weight_animals()

    def _die_stage(self):
        """
        die all the animals that are with higher probability in all cells
        """
        rows, cols = self.cells_dims
        for x in range(rows):
            for y in range(cols):
                self._cells[x, y].die_animals()

    def _migrate_stage(self):
        """
        migrate all the animals in all cells
        """
        for [x, y], cell in np.ndenumerate(self._cells):
            cell.migrate(self._adj_cells(x, y))
