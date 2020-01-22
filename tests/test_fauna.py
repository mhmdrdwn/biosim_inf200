# -*- coding: utf-8 -*-

"""
Test set for fauna classes functionality and attributes.

"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

import pytest
from biosim.fauna import Herbivore, Carnivore
import numpy as np


class TestFauna:
    """
    This set of tests checks the Fauna class methods perform as expected
    as provided in modeling.
    """
    @pytest.fixture
    def gen_animal_data(self):
        """
        Two animals of the two different species (Herbivore, Carnivore) with
        predefined set of parameters

        Returns
        -------
        carn: Carnivore object
        herb: Herbivore object
        """
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
        np.random.seed(1)
        carn = Carnivore()
        carn.set_given_parameters(c_params)
        np.random.seed(1)
        herb = Herbivore()
        herb.set_given_parameters(h_params)
        return carn, herb

    def test_age(self, gen_animal_data):
        """
        Age increases one year after one year

        Parameters
        ----------
        gen_animal_data: Carnivore and Herbivore Objects

        """
        carn, herb = gen_animal_data
        assert carn.age == 0
        assert herb.age == 0
        herb.grow_up()
        assert herb.age == 1
        assert carn.age == 0
        carn.grow_up()
        carn.grow_up()
        assert herb.age == 1
        assert carn.age == 2

    def test_weight(self, gen_animal_data):
        """
        using the np.random.seed(1), the expected values should be as follows

        Parameters
        ----------
        gen_animal_data: Carnivore and Herbivore objects with predefined
        parameters

        """
        carn, herb = gen_animal_data
        assert carn.weight == pytest.approx(6.7613871182275105)
        assert herb.weight == pytest.approx(4.4365180454948625)

    def test_lose_weight(self, gen_animal_data):
        c, h = gen_animal_data
        c_pre_lose_weight = c.weight
        h_pre_lose_weight = h.weight
        c.lose_weight()
        h.lose_weight()
        c_post_lose_weight = c.weight
        h_post_lose_weight = h.weight
        assert c_pre_lose_weight - c_post_lose_weight == pytest.approx(
            2.028416135468253)
        assert h_pre_lose_weight - h_post_lose_weight == pytest.approx(
            1.3309554136484587)

    def test_fitness(self, gen_animal_data):
        carn, herb = gen_animal_data
        assert carn.fitness == pytest.approx(0.12530026078413622)
        assert 0 <= carn.fitness <= 1
        assert herb.fitness == pytest.approx(0.058318513061424215)
        assert 0 <= herb.fitness <= 1

    def test_move_probability(self, gen_animal_data):
        """
         By changing mu value, there should be a higher probability

         Parameters
         ----------
         gen_animal_data: Carnivore, Herbivore objects

         """
        np.random.seed(1)
        carn, herb = gen_animal_data
        assert not carn.move_prob
        assert not herb.move_prob
        np.random.seed(1)
        carn.set_given_parameters({'mu': 70})
        assert carn.move_prob

    def test_birth_probability(self, gen_animal_data):
        """
        If there is less than 2 animals in the cell, the probability should
        be false, and changing the number of animals using the seed,
        it should give a predefine probability.

        Parameters:
        ----------
        gen_animal_data: Carnivore, Herbivore objects

        """
        np.random.seed(1)
        carn, herb = gen_animal_data
        assert not carn.birth_prob(1)
        assert not herb.birth_prob(1)
        assert carn.birth_prob(50)
        assert herb.birth_prob(50)

    def test_death_probability(self, gen_animal_data):
        """
        Probability of death given parameter omega 1, will lead to probability
        higher than the first seed random number.

        Parameters
        ----------
        gen_animal_data : Carnivore, Herbivore Objects

        """
        np.random.seed(1)
        carn, herb = gen_animal_data
        carn.set_given_parameters({'omega': 1})
        herb.set_given_parameters({'omega': 1})
        assert carn.death_prob
        assert herb.death_prob

    def test_give_birth_lose_weight(self, gen_animal_data):
        carn, herb = gen_animal_data
        carn_baby = Carnivore(weight=2)
        herb_baby = Herbivore(weight=1)
        carn.lose_weight_give_birth(carn_baby)
        herb.lose_weight_give_birth(herb_baby)

        assert carn.weight == pytest.approx(4.5613871182275103)
        assert herb.weight == pytest.approx(3.2365180454948623)

    def test_eat(self, gen_animal_data):
        """
        The weights after eating should increase

        Parameters
        ----------
        gen_animal_data: Carnivore and Herbivore objects

        """
        carn, herb = gen_animal_data
        c_pre_eat_weight = carn.weight
        h_pre_eat_weight = herb.weight
        carn.eat(20)
        herb.eat(30)
        c_post_eat_weight = carn.weight
        h_post_eat_weight = herb.weight
        assert c_post_eat_weight > c_pre_eat_weight
        assert h_post_eat_weight > h_pre_eat_weight
        assert c_post_eat_weight - c_pre_eat_weight == pytest.approx(4)
        assert h_post_eat_weight - h_pre_eat_weight == pytest.approx(9)


class TestHerbivores(TestFauna):
    """
    This set of tests checks the Herbivore class methods perform as expected
    as provided in modeling.
    """
    def test_parameters_set(self, gen_animal_data):
        """
        Parameters setting using the class method provided for the relevent
        class that is being instantiated.
        Parameters
        ----------
        gen_animal_data: Carnivore and Herbivore objects

        """
        carn, herb = gen_animal_data
        c_default_eta = carn.parameters['eta']
        h_default_beta = herb.parameters['beta']
        c_params = {'eta': 0.4}
        h_params = {'beta': 0.5}
        carn.set_given_parameters(c_params)
        herb.set_given_parameters(h_params)
        assert c_default_eta != carn.parameters['eta']
        assert h_default_beta != herb.parameters['beta']
        with pytest.raises(ValueError):
            carn.set_given_parameters({'eta': 1.1})
        with pytest.raises(ValueError):
            carn.set_given_parameters({'DeltaPhiMax': 0})
        with pytest.raises(ValueError):
            carn.set_given_parameters({'xi': -1})
        with pytest.raises(RuntimeError):
            carn.set_given_parameters({'new_var': 1})


class TestCarnivores(TestFauna):
    """
    This set of tests checks the Carnivore class methods perform as expected
    as provided in modeling.
    """
    def test_kill_probability(self, gen_animal_data):
        """
        The given weights shows that the herb is more fit than the carn.
        so, the probability should be false.
        ----------
        gen_animal_data: Carnivore and Herbivore objects

        """
        np.random.seed(1)
        carn = Carnivore(weight=10)
        herb = Herbivore(weight=100)
        assert not carn.kill_prob(herb)
