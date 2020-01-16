# -*- coding: utf-8 -*-

"""
Test set for Animals class functionality.

This set of tests checks the Animals class methods perform as expected as per
the provided modeling.

"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

import pytest
from biosim.fauna import Herbivore, Carnivore
from random import seed


class TestFauna:

    @pytest.fixture
    def gen_animal_data(self):
        c_params = {'eta': 0.30,
                    'w_birth': 4.0,
                    'sigma_birth': 1.7,
                    'w_half': 10,
                    'phi_age': 0.4,
                    'phi_weight': 0.6,
                    'a_half': 60,
                    'beta': 0.2,
                    'DeltaPhiMax': 11.0,
                    'mu': 0.25,
                    'gamma': 0.6,
                    'zeta': 1,
                    'omega': 0.6
                    }
        h_params = {'eta': 0.30,
                    'w_birth': 2.0,
                    'sigma_birth': 1.5,
                    'w_half': 10,
                    'phi_age': 0.3,
                    'phi_weight': 0.5,
                    'a_half': 40,
                    'beta': 0.3,
                    'mu': 0.3,
                    'gamma': 0.7,
                    'zeta': 1,
                    'omega': 0.3
                    }
        seed(1)
        c = Carnivore(params=c_params)
        seed(1)
        h = Herbivore(params=h_params)
        return c, h

    def test_age(self, gen_animal_data):
        c, h = gen_animal_data
        assert c.age == 0
        assert h.age == 0
        h.grow_up()
        assert h.age == 1
        assert c.age == 0
        c.grow_up()
        c.grow_up()
        assert h.age == 1
        assert c.age == 2
        # age increases one year after one year

    def test_weight(self, gen_animal_data):
        # basic random test, we need advanced tests
        c, h = gen_animal_data
        assert c.weight == 6.189914080364287
        assert h.weight == 3.9322771297331944
        # initial weight should be a function that is decorated as variable
        # it's following Gaussain distro, the seed 1 will generate that value

    def test_reduce_weight(self, gen_animal_data):
        c, h = gen_animal_data
        c_pre_reduce_weight = c.weight
        h_pre_reduce_weight = h.weight
        c.reduce_weight(2)
        h.reduce_weight(2)
        c_post_reduce_weight = c.weight
        h_post_reduce_weight = h.weight
        assert c_pre_reduce_weight - c_post_reduce_weight == 2
        assert h_pre_reduce_weight - h_post_reduce_weight == 2

    def test_grow_up(self, gen_animal_data):
        c, h = gen_animal_data
        c_weight_before_grow = c.weight
        h_weight_before_grow = h.weight
        c.grow_up()
        h.grow_up()
        c_weight_after_grow = c.weight
        h_weight_after_grow = h.weight
        assert c_weight_before_grow - c_weight_after_grow == pytest.approx(
            1.856974224109286)
        assert h_weight_before_grow - h_weight_after_grow == pytest.approx(
            1.1796831389199582)
        # weight weight by eta factor every year

    def test_fitness(self, gen_animal_data):
        c, h = gen_animal_data
        assert c.fitness == pytest.approx(0.09228477266076363)
        assert 0 <= c.fitness <= 1
        assert h.fitness == pytest.approx(0.04591907551573919)
        assert 0 <= h.fitness <= 1


    def test_move_probability(self, gen_animal_data):
        c, h = gen_animal_data
        assert c.move_probability == pytest.approx(0.023071193165190906)
        assert h.move_probability == pytest.approx(0.013775722654721757)

    def test_birth_probability(self, gen_animal_data):
        c, h = gen_animal_data
        assert c.birth_probablity(1) == 0
        assert h.birth_probablity(1) == 0
        # probablity is zero if animals is less than 2
        # probablity should be more than 0 if animals >= 2
        # probablity of giving birth if there are two animals in the cell
        assert c.birth_probablity(2) == pytest.approx(0.055370863596458174)
        assert h.birth_probablity(2) == pytest.approx(0.03214335286101743)
        # probability should be 0 if the weight is less than
        # zeta(w_birth+sigma_birth)
        h.parameters['zeta'] = 5
        c.parameters['zeta'] = 4
        assert c.birth_probablity(2) == 0
        assert h.birth_probablity(2) == 0

    def test_death_probability(self, gen_animal_data):
        c, h = gen_animal_data
        assert c.death_probability() == 0.5446291364035418
        assert h.death_probability() == 0.2862242773452782
        # probablity of death given fitness 0.1 will be 0.36

    def test_eat(self, gen_animal_data):
        c, h = gen_animal_data
        c_pre_eat_weight = c.weight
        h_pre_eat_weight = h.weight
        c.eat(20)
        h.eat(30)
        c_post_eat_weight = c.weight
        h_post_eat_weight = h.weight
        assert c_post_eat_weight > c_pre_eat_weight
        assert h_post_eat_weight > h_pre_eat_weight
        assert c_post_eat_weight - c_pre_eat_weight == pytest.approx(4)
        assert h_post_eat_weight - h_pre_eat_weight == pytest.approx(9)


class TestHerbivores(TestFauna):
    def test_parameters_set(self, gen_animal_data):
        c, h = gen_animal_data
        c_default_eta = c.parameters['eta']
        h_default_beta = h.parameters['beta']
        c_params = {'eta': 0.4}
        h_params = {'beta': 0.5}
        c.set_given_parameters(c_params)
        h.set_given_parameters(h_params)
        assert c_default_eta != c.parameters['eta']
        assert h_default_beta != h.parameters['beta']


class TestCarnivores(TestFauna):
    def test_kill_probability(self, gen_animal_data):
        c, h = gen_animal_data
        assert c.kill_probablity(h) == pytest.approx(0.004215063376820403)
