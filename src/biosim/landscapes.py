# -*- coding: utf-8 -*-

"""
Landscape Class and subclasses (Jungle, Desert, Ocean, Savannah, Mountain).
Landscape class is a base class, all objects are instantiated from the
Jungle, Desert, Ocean, Savannah, Mountain subclasses
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from abc import ABC, abstractmethod
import operator
import math
import numpy as np


class Landscape(ABC):
    """
    Landscape abstract class. It has five subclasses: Jungle, Desert,
    Savannah, Ocean, Mountain inherited from this base class.
    """
    parameters = {}

    @abstractmethod
    def __init__(self):
        self._available_fodder = {'Herbivore': 0, 'Carnivore': 0}
        self.in_cell_fauna = {'Herbivore': [], 'Carnivore': []}
        self.adult_fauna = {'Herbivore': [], 'Carnivore': []}

    def sort_by_fitness(self):
        """
        Sorts animal objects of each species according to their fitness.
        """
        self.in_cell_fauna['Carnivore'].sort(
            key=operator.attrgetter('fitness'), reverse=True)
        self.in_cell_fauna['Herbivore'].sort(
            key=operator.attrgetter('fitness'))

    def relevant_fodder(self, animal):
        """
        Amount of f_k which is relevant fodder in cell k regarding animal
        species.
        Parameters
        ----------
        animal: Carnivore or Herbivore object
        Returns
        -------
        available_fodder[species]: float
            Available fodder (f_k) regarding the animal species of cell k
        """
        species = animal.__class__.__name__
        return self.available_fodder[species]

    def relative_abundance_fodder(self, animal):
        """
        Calculates "Relative Abundance of Fodder" (E_k) that is calculated
        based on relevant fodder, number of animals of that kind and the
        F which is a given parameter from the species' subclass.
        Parameters
        ----------
        animal: Carnivore or Herbivore object
        Returns
        -------
        relative abundance fodder: float
            Relative abundance of fodder of cell k
        """
        species = animal.__class__.__name__
        return self.relevant_fodder(animal) / (
                (len(self.in_cell_fauna[species]) + 1)
                * animal.parameters['F'])

    def propensity(self, animal):
        """
        Returns propensity to move from i which is calculated for all of four
        adjacent cells as j.
        - When j is mountain or ocean, the propensity is zero.
        - Otherwise, it is computed as below equation: e ^ ('lambda' * E_j)
        Parameters
        ----------
        animal: Carnivore or Herbivore object
        Returns
        -------
        propensity: float
            propensity to move from i to j
        """
        if isinstance(self, Mountain) or isinstance(self, Ocean):
            return 0
        else:
            relevant_abun_fodder = self.relative_abundance_fodder(animal)
            return math.exp(relevant_abun_fodder *
                            animal.parameters['lambda'])

    def probability(self, animal, total_propensity):
        """
        Returns the corresponding probability to move from i to j based on the
        given total propensity of all adjacent cells
        Parameters
        ----------
        animal: Carnivore or Herbivore object
        total_propensity: float
        Returns
        -------
        Probability: float
        """
        return self.propensity(animal) / total_propensity

    def add_animal(self, animal):
        """
        Adds the new object of animal to the list of same species of the cell.
        Parameters
        ----------
        animal: Carnivore or Herbivore object
        """

        key = animal.__class__.__name__
        self.in_cell_fauna[key].append(animal)

    def remove_animal(self, animal):
        """
        Removes the object of animal from the list of same species of the cell.
        Parameters
        ----------
        animal: object?
        """
        species = animal.__class__.__name__
        self.in_cell_fauna[species].remove(animal)

    @property
    def cell_fauna_count(self):
        """
        Calculates the number of fauna by their species and gives animal
        dictionary of animal with species keys
        Returns
        -------
        dictionary of animal with species keys
        """
        herbivore = len(self.in_cell_fauna['Herbivore'])
        carnivore = len(self.in_cell_fauna['Carnivore'])
        return {'Herbivore': herbivore, 'Carnivore': carnivore}

    def _feed_herbivore(self):
        """
        Herbivores with the highest fitness eat first, "sorted_fauna_fitness"
         dictionary is reverse sorted .
        Every time a herbivore eats, the animal can eat fodder as the following
        "eating rules":
        - If available fodder is more than 'F', the animal eats 'F' and the
          amount of fodder in the cell is reduced by F.
        - When available fodder is less than 'F' , the animal eats what is left
          of fodder and the remain fodder is set to zero.
        - If there is no fodder, the animal receives no food.
        """
        self.sort_by_fitness()
        for herbivore in self.in_cell_fauna['Herbivore']:
            herb_available_fodder = self.available_fodder['Herbivore']
            appetite = herbivore.parameters['F']
            if herb_available_fodder == 0:
                # break the loop to save computation
                break
            elif herb_available_fodder >= appetite:
                herbivore.eat(appetite)
                self.available_fodder['Herbivore'] -= appetite
            elif 0 < herb_available_fodder < appetite:
                amount_to_eat = self.available_fodder['Herbivore']
                herbivore.eat(amount_to_eat)
                self.available_fodder['Herbivore'] = 0

    def _feed_carnivore(self):
        """
        Carnivores with the highest fitness eat first. The method
        "sort_by_fitness" return reverse sorted carnivores by fitness.
        Herbivores are sorted.
        A carnivore continues to kill herbivores until one of the following
        conditions occur:
        - The carnivore has eaten herbivores with a total weight of 'F'
        - Or, it has tried to kill each herbivore in the cell.
        """
        self.sort_by_fitness()
        for carnivore in self.in_cell_fauna['Carnivore']:
            appetite = carnivore.parameters['F']
            amount_to_eat = 0
            not_eaten_animals = []
            for i, herbivore in enumerate(self.in_cell_fauna['Herbivore']):
                if appetite <= amount_to_eat:
                    not_eaten_animals.extend(self.in_cell_fauna
                                             ['Herbivore'][i:])
                    break
                elif carnivore.kill_prob(herbivore):
                    if appetite - amount_to_eat < herbivore.weight:
                        amount_to_eat += herbivore.weight
                    elif appetite - amount_to_eat < herbivore.weight:
                        amount_to_eat += appetite - amount_to_eat
                else:
                    not_eaten_animals.append(herbivore)
            carnivore.eat(amount_to_eat)
            self.in_cell_fauna['Herbivore'] = not_eaten_animals

    def feed_animals(self):
        """
        call for functions all carnivore and herbivore animals in the cell
        to eat
        """
        self._grow_herb_fodder()
        self._feed_herbivore()
        self._feed_carnivore()

    def _grow_herb_fodder(self):
        pass

    def grow_up_animals(self):
        """
        Runs grow_up method from Fauna class to do yearly aging of all animals
        in the cell.
        """
        for species in self.in_cell_fauna:
            for animal in self.in_cell_fauna[species]:
                animal.grow_up()

    def lose_weight_animals(self):
        """
        Runs lose_weight method from Fauna class to do yearly weight loss of
        all animals in the cell.
        """
        for species in self.in_cell_fauna:
            for animal in self.in_cell_fauna[species]:
                animal.lose_weight()

    def die_animals(self):
        """
        Removes the animal object from the animals' dictionary, if the random
        number is more than or equal to death probability for that object
        in the cell.
        """
        for species, animals in self.in_cell_fauna.items():
            for animal in animals:
                if animal.death_prob:
                    self.remove_animal(animal)

    def add_baby_to_adult_animals(self):
        """
        After the breeding stage, the new babies are added to the cell
        animals dictionary and remove it from the baby fauna dictionary.
        adult_fauna as input to calculate the giving birth probability.
        """

        self.adult_fauna = self.in_cell_fauna

    def give_birth_animals(self):
        """
        Adds new object of baby to the animals' dictionary of same kind, and
        decreases mother's weight when random number for group of two animals
        of same kind in the cell is more than or equal to birth probability.
        Only adult fauna are allowed to give birth. Babies animals are added
        to the dictionary of animals in cells. But it's allowed to give birth
        in the first year of the cycle. But added to the adult animals for the
        next year
        """

        for species, animals in self.adult_fauna.items():
            half_num_fauna = math.floor(len(self.adult_fauna[species]) / 2)
            # half of the animals will give birth of adult animals
            for i in range(half_num_fauna):
                animal = animals[i]
                # only iterate through the first half of the animal list
                if animal.birth_prob(len(animals)):
                    baby_species = animal.__class__
                    baby = baby_species()
                    animal.lose_weight_give_birth(baby)
                    if animal.just_give_birth:
                        self.in_cell_fauna[species].append(baby)
                        animal.just_give_birth = False

    def migrate(self, adj_cells):
        """
        Moves the object from i to j by generating random number and comparing
        first with movement probability and then the probability to move from i
        to j and removes it from current cell (i). If total propensity if 0,
        animals won't move since that adjacent cells are inaccessible.
        Animals migrate to the cell with first accumulated propability that is
        higher than the random number.
        Parameters
        ----------
        adj_cells: list
            List of 4 adjacent cells
        """
        adj_cells = np.array(adj_cells)
        for species, animals in self.in_cell_fauna.items():
            for animal in animals:
                if animal.move_prob:
                    propensity = [cell.propensity(animal) for cell in
                                  adj_cells]
                    total_propensity = sum(propensity)
                    if total_propensity != 0:
                        probability = [cell.probability(animal,
                                                        total_propensity)
                                       for cell in adj_cells]
                        cum_probability = np.cumsum(probability)
                        random_num = np.random.random()
                        i = 0
                        while random_num > cum_probability[i]:
                            i += 1
                        cell_to_go = adj_cells[i]
                        if cell_to_go.is_accessible:
                            cell_to_go.add_animal(animal)
                            self.remove_animal(animal)

    @classmethod
    def set_given_parameters(cls, given_parameters):
        """
        Sets the user defined parameters that applies to Savannah, Jungle.
        Parameters
        ----------
        given_parameters: dict
        """

        for parameter in given_parameters:
            if parameter in Savannah.parameters:
                cls.parameters[parameter] = \
                    given_parameters[parameter]
            else:
                raise RuntimeError('Unknown parameter, ' +
                                   str(parameter) +
                                   ' can\'t be set')

    @property
    def total_herb_weight(self):
        return sum(i.weight for i in self.in_cell_fauna['Herbivore'])

    @property
    def available_fodder(self):
        if isinstance(self, (Ocean, Mountain)):
            raise ValueError('There are no fodder available in this cell')
        elif isinstance(self, Desert):
            self._available_fodder = {'Herbivore': 0,
                                      'Carnivore': self.total_herb_weight}
        else:
            self._available_fodder = {'Herbivore': self.parameters['f_max'],
                                      'Carnivore': self.total_herb_weight}
        return self._available_fodder


class Savannah(Landscape):
    """
    Subclass of Landscape with fodder growth rate of
    alpha * ('f_max'- available_fodder)
    """
    is_accessible = True
    parameters = {'f_max': 300.0, 'alpha': 0.3}

    def __init__(self, given_parameters=None):
        """
        Subclass of Landscape
        Parameters
        ----------
        given_parameters: dict
        """
        super().__init__()
        if given_parameters is not None:
            self.set_given_parameters(given_parameters)
        self.parameters = Savannah.parameters

    def _grow_herb_fodder(self):
        """
        Calculates new fodder growing in savannah according to the following
        equation:
        available_fodder + 'alpha' * ('f_max'- available_fodder)
        """
        self.available_fodder['Herbivore'] += \
            self.parameters['alpha'] * (self.parameters['f_max'] -
                                        self.available_fodder['Herbivore'])


class Jungle(Landscape):
    """
    The jungle is accessible by animals. Main difference in jungle is that
    the fodder reset to f_max each year
    """
    is_accessible = True
    parameters = {'f_max': 300.0}

    def __init__(self, given_parameters=None):
        """
        saving the predefined parameters in the class variable.
        Parameters
        ----------
        given_parameters: dict
        """
        super().__init__()
        if given_parameters is not None:
            self.set_given_parameters(given_parameters)
        self.parameters = Jungle.parameters

    def _grow_herb_fodder(self):
        """
        Resets a fixed amount of fodder 'f_max' to available_fodder
        of herbivore.
        """
        self.available_fodder['Herbivore'] = self.parameters['f_max']


class Desert(Landscape):
    """
    Animals may stay in the desert, but there is no fodder available to
    herbivores there.
    Carnivores can prey on herbivores in the desert.
    """
    is_accessible = True

    def __init__(self):
        super().__init__()


class Mountain(Landscape):
    """
    The mountain can not be entered by animals. So that, the animal lists are
    always empty for this kind of landscape and there is no fodder.
    """

    is_accessible = False

    def __init__(self):
        super().__init__()


class Ocean(Landscape):
    """
    The ocean can not be entered by animals. So that, the animal lists are
    always empty for this kind of landscape and there is no fodder.
    """

    is_accessible = False

    def __init__(self):
        super().__init__()
