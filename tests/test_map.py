# -*- coding: utf-8 -*-

"""
Test set for Map class functionality and attributes.

"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from random import seed

import pytest

from biosim.landscapes import Desert, Ocean, Mountain, Savannah, Jungle
from biosim.fauna import Herbivore, Carnivore
from biosim.map import Map


class TestMap:
    """
    This set of tests checks the map class methods perform as expected
    as provided in modeling.

    """
    @pytest.fixture
    def gen_animal_data(self):
        seed(1)
        h1 = Herbivore()
        h2 = Herbivore()
        seed(1)
        c1 = Carnivore()
        c2 = Carnivore()
        return c1, c2, h1, h2

    @pytest.fixture
    def gen_landscape_data(self, gen_animal_data):
        c1, c2, h1, h2 = gen_animal_data
        landscapes_dict = {'s': Savannah(),
                           'o': Ocean(),
                           'd': Desert(),
                           'm': Mountain(),
                           'j': Jungle()}
        return landscapes_dict

    @pytest.fixture
    def gen_map_data(self, gen_landscape_data):
        map_str = """          OOOOOOOOOOOOOOOOOOOOO
                               OMSOOOOOSMMMMJJJJJJJO
                               OOOOOOOOOOOOOOOOOOOOO"""
        m = Map(map_str)
        return m

    def test_string_to_np_array(self):
        """
        output of the function is np.ndarray and the letters are in the
        right row/column in the matrix

        """
        map_str = """  OOOOOOOOOOOOOOOOOOOOO
                       OMSOOOOOSMMMMJJJJJJJO
                       OOOOOOOOOOOOOOOOOOOOO"""
        m = Map(map_str)
        assert m.string_to_np_array()[0][0] == 'O'
        assert m.string_to_np_array()[1][10] == 'M'
        assert m.string_to_np_array()[1][20] == 'O'
        assert type(m.string_to_np_array()).__name__ == 'ndarray'

    def test_create_map(self):
        """
        Object matches with the given string

        """
        map_str = """  OOOOOOOOOOOOOOOOOOOOO
                       OMSOOOOOSMMMMJJJJJJJO
                       OOOOOOOOOOOOOOOOOOOOO"""
        m = Map(map_str)
        assert isinstance(m.create_map_of_landscape_objects()[0][0], Ocean)
        assert isinstance(m.create_map_of_landscape_objects()[1][10], Mountain)
        assert isinstance(m.create_map_of_landscape_objects()[1][20], Ocean)
        assert isinstance(m.create_map_of_landscape_objects()[1][2], Savannah)

    def test_adj_cells(self):
        """
        test that all adjacent elements are only the perpendicular cells

<<<<<<< Updated upstream
        """
        map_str = """  OOOOOOOOOOOOOOOOOOOOO
                       OMSOOOOOSMMMMJJJJJJJO
                       OOOOOOOOOOOOOOOOOOOOO"""
        m = Map(map_str)
        m.string_to_np_array()
        assert all(j in m.adj_cells(0, 0) for j in ['O', 'O'])
        assert all(j in m.adj_cells(1, 0) for j in ['M', 'O', 'O'])
        assert all(j in m.adj_cells(2, 20) for j in ['O', 'O'])

    def test_not_surrounded_by_ocean(self):
        """
        the constructor raise value error incase the map string is not
        surrounded by letter 'O'

        """
        map_str = """    OSOOOOOOOOOOOOOOOOOOO
                         OMSOOOOOSMMMMJJJJJJJO
                         OOOOOOOOOOOOOOOOOOOOO"""

        with pytest.raises(ValueError) as err:
            m = Map(map_str)
        assert err.type is ValueError

    def test_add_animals(self, gen_map_data):
        """
        Add animals and check the total number of animals

        """
        m = gen_map_data
        print(m)
        animals = [
            {
                "loc": (1, 1),
                "pop": [
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                    {"species": "Carnivore", "age": 1, "weight": 10.0},
                ],
            },
            {
                "loc": (1, 2),
                "pop": [
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                    {"species": "Carnivore", "age": 1, "weight": 10.0},
                ],
            },
        ]
        m.add_animals(animals)
        assert m.total_num_animals_per_species('Herbivore') == 2
        assert m.total_num_animals_per_species('Carnivore') == 2

    def test_die_stage(self, gen_map_data):
        """
        number of animals should decrease after die
        Parameters
        ----------
        gen_map_data: Map object

        """
        m = gen_map_data
        num_animals_before = m.total_num_animals_per_species('Herbivore')
        m.life_cycle()
        num_animals_after = m.total_num_animals_per_species('Herbivore')
        assert num_animals_after <= num_animals_before

    def test_give_birth_stage(self, gen_map_data):
        """
        number of animals should increase after procreation

        Parameters
        ----------
        gen_map_data: Map object

        -------

        """
        m = gen_map_data
        num_animals_before = m.total_num_animals_per_species('Herbivore')
        m.give_birth_stage()
        num_animals_after = m.total_num_animals_per_species('Herbivore')
        assert num_animals_after >= num_animals_before
=======
>>>>>>> Stashed changes
