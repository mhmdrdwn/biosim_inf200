# -*- coding: utf-8 -*-

"""
Test set for landscapes class functionality and attributes.

This set of tests checks the landscapes classes methods perform as expected as per
the provided modeling.

"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from random import seed
from biosim.fauna import Carnivore, Herbivore
from biosim.simulation import BioSim
import pytest
import textwrap


class TestSimulation:
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
        c1 = Carnivore()
        h1 = Herbivore()
        c_pre_change_xi = c1.parameters['xi']
        h_pre_change_xi = h1.parameters['xi']
        biosim.set_animal_parameters('Carnivore', {'xi': 1.8})
        c2 = Carnivore()
        h2 = Herbivore()
        assert c_pre_change_xi == 1.1
        assert h_pre_change_xi == 1.2
        assert c1.parameters['xi'] == 1.8
        assert c2.parameters['xi'] == 1.8
        assert h2.parameters['xi'] == 1.2
        with pytest.raises(TypeError) as err:
            biosim.set_animal_parameters("dog", {"xi": 1.8})
        assert err.type is TypeError

    def test_set_landscape_parameters(self, gen_simulation_data):
        biosim = gen_simulation_data
        biosim.set_landscape_parameters()
        #assert c_pre_change_xi == 1.1
        #assert h_pre_change_xi == 1.2
        #assert c1.parameters['xi'] == 1.8
        #assert c2.parameters['xi'] == 1.8
        #assert h2.parameters['xi'] == 1.2
        #with pytest.raises(ValueError) as err:
        #    biosim.set_landscape_parameters("dog", {"xi": 1.8})
        #assert err.type is ValueError
