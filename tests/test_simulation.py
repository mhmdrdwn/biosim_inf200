# -*- coding: utf-8 -*-

"""
Test set for Simulation class functionality and attributes.

"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from biosim.fauna import Carnivore, Herbivore
from biosim.landscapes import Savannah, Desert, Ocean, Mountain, Jungle
from biosim.map import Map
from biosim.simulation import BioSim
import pytest


class TestSimulation:
    """
    This set of tests checks the Simulation class methods perform as expected as
    provided in modeling.
    """
    @pytest.fixture
    def gen_simulation_data(self):
        import textwrap

        geogr = """\
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
        geogr = textwrap.dedent(geogr)
        ini_herbs = [
            {
                "loc": (10, 10),
                "pop": [
                    {"species": "Herbivore", "age": 5, "weight": 20}
                    for _ in range(3)
                ],
            }
        ]
        ini_carns = [
            {
                "loc": (20, 20),
                "pop": [
                    {"species": "Carnivore", "age": 5, "weight": 20}
                    for _ in range(5)
                ],
            }
        ]
        ini_carns2 = [
            {
                "loc": (10, 10),
                "pop": [
                    {"species": "Carnivore", "age": 5, "weight": 20}
                    for _ in range(4)
                ],
            }
        ]
        ini_carns3 = [
            {
                "loc": (30, 30),
                "pop": [
                    {"species": "Carnivore", "age": 5, "weight": 20}
                    for _ in range(5)
                ],
            }
        ]
        ini_carns4 = [
            {
                "loc": (40, 40),
                "pop": [
                    {"species": "Carnivore", "age": 5, "weight": 20}
                    for _ in range(5)
                ],
            }
        ]
        biosim = BioSim(island_map=geogr, ini_pop=ini_herbs, seed=123456)
        return biosim

    def test_set_animal_parameters(self, gen_simulation_data):
        biosim = gen_simulation_data
        c = Carnivore()
        h = Herbivore()
        c_pre_change_xi = c.parameters['xi']
        h_pre_change_xi = h.parameters['xi']
        biosim.set_animal_parameters('Carnivore', {'xi': 1.8})
        assert c_pre_change_xi == 1.1
        assert h_pre_change_xi == 1.2
        assert c.parameters['xi'] == 1.8
        assert h.parameters['xi'] == 1.2
        with pytest.raises(TypeError) as err:
            biosim.set_animal_parameters("dog", {"xi": 1.8})
        assert err.type is TypeError

    def test_set_landscape_parameters(self, gen_simulation_data):
        biosim = gen_simulation_data
        c1 = Carnivore()
        h1 = Herbivore()
        c2 = Carnivore()
        h2 = Herbivore()
        animals = {'Herbivore': [h1, h2], 'Carnivore': [c1, c2]}
        s = Savannah(animals)
        assert s.parameters['f_max'] == 300
        biosim.set_landscape_parameters("S", {"f_max": 700})
        assert s.parameters['f_max'] == 700
        with pytest.raises(ValueError) as err:
            biosim.set_landscape_parameters('O', {'f_max': 1.8})
        assert err.type is ValueError
        with pytest.raises(TypeError) as err:
            biosim.set_landscape_parameters('P', {'f_max': 1.8})
        assert err.type is TypeError

    def test_add_population(self, gen_simulation_data):
        biosim = gen_simulation_data
        carns = [
            {
                "loc": (40, 40),
                "pop": [
                    {"species": "Carnivore", "age": 5, "weight": 20}
                    for _ in range(5)
                ],
            }
        ]
        assert len(Map.all_fauna) == 0
        biosim.add_population(carns)
        assert len(Map.all_fauna) == 1
