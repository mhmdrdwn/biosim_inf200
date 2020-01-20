# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from abc import ABC, abstractmethod
import operator

import math
import numpy as np

from biosim.fauna import Herbivore, Carnivore


class Landscape(ABC):
    """
    Landscape abstract class. There are five subclasses: Jungle, Desert,
    Savannah, Ocean, Mountain inherited from this base class.
    """
    available_fodder = {}
    parameters = {}

    @abstractmethod
    def __init__(self):
        # those fauna list is given from the map, which was given earlier
        # from the simulation as initial animals and we append it to when
        # migration and birthing
        self._in_cell_fauna = {'Herbivore': [], 'Carnivore': []}
        # that should be list of dicts
        self.sorted_fauna_fitness = {}

    def save_fitness(self, fauna_objects, species):
        """
        Updating the current fitness and sort.

        Parameters
        ----------
        fauna_objects: dict
        species: str ?

        Returns
        -------
        ?
        """
        # this is to update the current fitness to be able to use in
        # the order later
        # remember also that fitness is goijg to change each time they eat
        species_fauna_fitness = {}
        # saving the data only for the species that we want to save,
        # not for all
        for fauna in fauna_objects[species]:
            species_fauna_fitness[fauna] = fauna.fitness
        self.sorted_fauna_fitness[species] = species_fauna_fitness

    def sort_by_fitness(self, animal_objects, species_to_sort, reverse=True):
        """
        Sorts animal objects of each species according to their fitness whether
        it can be sorted or reverse sorted.

        Parameters
        ----------
        animal_objects: dict? or list
        species_to_sort: str
        reverse: bool
        """
        self.save_fitness(animal_objects, species_to_sort)
        if reverse:
            self.sorted_fauna_fitness[species_to_sort] = dict(
                sorted(self.sorted_fauna_fitness[species_to_sort].items(),
                       key=operator.itemgetter(1), reverse=True))
        else:
            self.sorted_fauna_fitness[species_to_sort] = dict(
                sorted(self.sorted_fauna_fitness[species_to_sort].items(),
                       key=operator.itemgetter(1)))
        # all fitnesses is sorted for the animals in species, depends on the
        # parameters whether it should be sorted or reverse sorted

    def relevant_fodder(self, animal):
        """
        Returns relevant fodder in cell k (f_k) regarding animal species.

        Parameters
        ----------
        animal: object

        Returns
        -------
        available_fodder[species]: float ?
        """
        # This is f_k
        species = animal.__class__.__name__
        return self.available_fodder[species]
        # remember each time a carni move, number of herbi is
        # differnt in the cells, since they travel based on fitness
        # maybe a herbi is higher fitness

    def relative_abundance_fodder(self, animal):
        """
        Calculates "Relative Abundance of Fodder" (E_k) which is
        used in computing propensity to move. That is calculated based on f_k,
        number of animals of that kind and the F which is a given parameter from
        the species' subclass.

        Parameters
        ----------
        animal: ?
        """
        species = animal.__class__.__name__
        return self.relevant_fodder(animal) / (
                (len(self._in_cell_fauna[species]) + 1) *
                animal.parameters['F'])
        # we instantiate object of teh species given and get F from it
        # maybe there is error here

    def propensity(self, animal):
        """
        Returns propensity to move from i which is calculating for all of four
        adjacent cells. When j is mountain or ocean, the propensity is
        zero. Otherwise, it is computed as below equation:
        e ^ ('lambda' * E_j)

        Parameters
        ----------
        animal: ?
        """
        if isinstance(self, Mountain) or isinstance(self, Ocean):
            return 0
        else:
            relevant_abun_fodder = \
                self.relative_abundance_fodder(animal)
            return math.exp(relevant_abun_fodder *
                            animal.parameters['lambda'])

    def probability_of_cell(self, animal, total_propensity):
        """
        Returns the corresponding probability to move from i to j.

        Parameters
        ----------
        animal: object
        total_propensity: float
        """
        return self.propensity(animal) / total_propensity
        # this is the rule of probablity

        # if animal_object.parameters['lambda'] == 0:
        # all possible distination will be cjosen with equal probablity
        # elif animal_object.parameters['lambda'] == 0:
        # animals will go to cell with greater abundance of food
        # else:
        # animals will turn away from food

    def add_animal(self, animal):
        """
        Adds the new object of animal to the list of same species of the cell.

        Parameters
        ----------
        animal: object?
        """
        key = animal.__class__.__name__
        self._in_cell_fauna[key].append(animal)

    def remove_animal(self, animal):
        """
        Removes the object of animal from the list of same species of the cell.

        Parameters
        ----------
        animal: object?
        """
        key = animal.__class__.__name__
        self._in_cell_fauna[key].remove(animal)

    @property
    def cell_fauna_count(self):
        """
        Calculates the number of fauna by their species.
        """
        herbivore = len(self._in_cell_fauna['Herbivore'])
        carnivore = len(self._in_cell_fauna['Carnivore'])
        return {'Herbivore': herbivore, 'Carnivore': carnivore}

    def mate(self, animal):
        """
        Breeding new baby, if random number is bigger than the birth probability
         and also if the weight of mother is more than the weight she loses.

        Parameters
        ----------
        animal: obj?
        """
        # now change the population of the cell
        # decrease the weight of the mother
        species = animal.__class__
        num_fauna = len(self._in_cell_fauna[species.__name__])
        if np.random.random() > animal.birth_prob(num_fauna):
            # if that random number is bigger than that probablity it should
            # give birth, or create new baby, or object of animal
            baby = species()
            if animal.weight < baby.parameters['w_birth'] * \
                    baby.parameters['xi']:
                # it gives birth only if its weight is more than the the
                # weight to be losed
                self.add_animal(baby)
                animal.give_birth(baby)
                # that's still wrong becuase it's with the weight of the baby
            else:
                pass
                # dont give birth ?

    def feed_herbivore(self):
        """
        Herbivores find fodder exclusively in the savannah and jungle. The
        animal with the highest fitness eating first.
        Each animal tries every year to eat an amount 'F' of fodder, but how
        much feed the animal obtain depends on fodder available in the cell.
        Every time a herbivore eats, the animal can eat fodder as the following
         "eating rules":
        If available fodder is more than 'F', the animal eats 'F' and the amount
        of fodder in the cell is reduced by F.
        While, when it is less than 'F' , the animal eats what is left of fodder
        and the remain fodder is set to zero.
        Finally, if there is no fodder, the animal receives no food.
        These rules are for both Jungle and Savannah landscapes.
        Also, because in Desert there is no fodder, the third rule applies.
        Animals can not go to Ocean or Mountain, so that the eating rules are
        not applicable for these landscapes.
        """
        # that should return the amount of food that is going to be
        # eaten by all animals in celll
        self.sort_by_fitness(self._in_cell_fauna, 'Herbivore')
        # we need to sort animals by fitness prior to the eating, and the
        # animals with highest fitness eats first
        for herbivore in self.sorted_fauna_fitness['Herbivore']:
            # this is already reverse sorted dictionary, so animals at the
            # beginning are the hight fitness
            # heribore is an object that is saved in the dictionary,
            # eat method is amethod in Fauna class
            # change the amount of avialable fadder in landscape after animal eats
            # eaten_food = 0
            herb_available_fodder = self.available_fodder['Herbivore']
            appetite = herbivore.parameters['F']
            if herb_available_fodder == 0:
                break
                # break the for-loop to save computation cost becuase it's no
                # longer effective to iterate through it and they will not
                # recieve any food
                # Animals here recieves no food
                # self._available_fodder = 0
                # last else statment is not required, so we can remove it and add
                # it to the elif
            elif herb_available_fodder >= appetite:
                # animals eat what he required
                herbivore.eat(appetite)
                self.available_fodder['Herbivore'] -= appetite
            elif 0 < herb_available_fodder < appetite:
                # animals eat what is left
                amount_to_eat = self.available_fodder['Herbivore']
                herbivore.eat(amount_to_eat)
                self.available_fodder['Herbivore'] = 0

    def feed_carnivore(self):
        """
        Carnivores can prey on herbivores everywhere, but do not prey on each
        other. Carnivores with the highest fitness eats first. Carnivores try
        to kill one herbivore at atime, beginning with the herbivore with the
        lowest fitness. A carnivore continues to kill herbivores until one of
        the following conditions occur:
        The carnivore has eaten herbivores with a total weight of 'F' or more
        than it. Or, it has tried to kill each herbivore in the cell.
        """
        self.sort_by_fitness(self._in_cell_fauna, 'Carnivore')
        self.sort_by_fitness(self._in_cell_fauna, 'Herbivore', False)
        # reverse order the carnivore by fitness and sort the herbivore
        for carnivore in self.sorted_fauna_fitness['Carnivore']:
            # carbivore with highest fitness will kill the lowest fitness
            # herbivore first and so on
            appetite = carnivore.parameters['F']
            if len(self.sorted_fauna_fitness['Herbivore']) > 0:
                # if available food (weight of herbi) is zero ,break the for loop becuase it's
                # no longer efficient
                for herbivore in self.sorted_fauna_fitness['Herbivore']:
                    # carnivore will kill herivore as a time
                    # if the
                    if np.random.random() > carnivore.kill_prob(
                            herbivore):
                        weight_to_eat = herbivore.weight
                        # del self.sorted_fauna_fitness['Herbivore'][herbivore]
                        # remove it from the dictionary, meaning removing from the cell
                        # herbivore.die()
                        # we need a good implimenetation for method die in the fauna
                        if weight_to_eat >= appetite:
                            # that's wrong becuase, the weight to eat is the weight
                            # of only one meal
                            carnivore.eat(appetite)
                        elif weight_to_eat < appetite:
                            carnivore.eat(weight_to_eat)

    def feed_animals(self):
        self.grow_herb_fodder()
        self.feed_herbivore()
        self.feed_carnivore()

    def grow_herb_fodder(self):
        return

    def migrate_animals(self, adj_cells):
        for species in self._in_cell_fauna:
            for animal in self._in_cell_fauna[species]:
                if np.random.random() > animal.move_prob:
                    cell_probabilities_list = [cell.probability_of_cell(animal)
                                               for cell in adj_cells]
                    maximum_probability_index = cell_probabilities_list.index(
                        max(cell_probabilities_list))
                    cell_with_maximum_probability = adj_cells[
                        maximum_probability_index]
                    self.remove_animal(animal)
                    cell_with_maximum_probability.add_fauna(animal)

    def grow_up_animals(self):
        for species in self._in_cell_fauna:
            for animal in self._in_cell_fauna[species]:
                animal.grow_up()

    def lose_weight_animals(self):
        for species in self._in_cell_fauna:
            for animal in self._in_cell_fauna[species]:
                animal.lose_weight()

    def die_animals(self):
        for species in self._in_cell_fauna:
            for animal in self._in_cell_fauna[species]:
                if np.random.random() > animal.death_prob():
                    self.remove_animal(animal)

    def give_birth_animals(self):
        for species in self._in_cell_fauna:
            for animal in self._in_cell_fauna[species]:
                if np.random.random() > animal.birth_prob:
                    baby_species = animal.__class__
                    baby = baby_species()
                    animal.give_birth(baby)


class Savannah(Landscape):
    """
    The savannah is accessible by animals. Also, It offers fodder for herbivores
    in limited quantity and is sensitive to overgrazing.
    Carnivores can prey on herbivores in the savannah.
    """
    is_accessible = True
    parameters = {'f_max': 300.0, 'alpha': 0.3}

    def __init__(self, given_parameters=None):
        """
        This is the constructor for the Savannah class, which is a subclass of
        Landscape class.


        Parameters
        ----------
        given_parameters: dict
        """
        super().__init__()
        if given_parameters is not None:
            self.set_given_parameters(given_parameters)
        self.parameters = Savannah.parameters
        self.available_fodder['Herbivore'] = self.parameters['f_max']
        total_herb_weight = sum(i.weight for i in
                                self._in_cell_fauna['Herbivore'])
        self.available_fodder['Carnivore'] = total_herb_weight
        # aviable fodder equals to f_max at the beginning of
        # instaniating anew object

    def grow_herb_fodder(self):
        """
        Every year in savannah, new fodder grows according to the following
        equation:
        available_fodder + 'alpha' * ('f_max'- available_fodder)

        Returns
        -------
        available_fodder: float or int ?

        """
        # annual grow of the fodder
        self.available_fodder['Herbivore'] += self.parameters['alpha'] \
                                              * (self.parameters['f_max']
                                                 - self.available_fodder[
                                                     'Herbivore'])

    @staticmethod
    def set_given_parameters(given_parameters):
        """
        Sets the user defined parameters that applies to Savannah.

        Parameters
        ----------
        given_parameters: dict
        """
        for parameter in given_parameters:
            if parameter in Savannah.parameters:
                Savannah.parameters[parameter] = \
                    given_parameters[parameter]
            else:
                # unknown parameter
                raise RuntimeError('Unknown parameter, ' +
                                   str(parameter) +
                                   ' can\'t be set')


class Jungle(Landscape):
    """
    The jungle is accessible by animals. Also, It offers fixed amount of fodder
    for herbivores annually and is not susceptible to long term damage due to
    overgrazing.
    Carnivores can prey on herbivores in the jungle.
    """
    is_accessible = True
    parameters = {'f_max': 300.0}

    def __init__(self, given_parameters=None):
        """

        Parameters
        ----------
        given_parameters: dict
        """
        super().__init__()
        if given_parameters is not None:
            self.set_given_parameters(given_parameters)
        self.parameters = Jungle.parameters
        self.available_fodder['Herbivore'] = self.parameters['f_max']
        total_herb_weight = sum(
            i.weight for i in self._in_cell_fauna['Herbivore'])
        self.available_fodder['Carnivore'] = total_herb_weight
        # amount of initial fodder aviable should equals to f_max

    def grow_herb_fodder(self):
        """
        In the jungle, the growth of vegetation is, however, so quick that each
        year, a fixed amount of fodder is available which is equal to 'f_max'


        Returns
        -------
        available_fodder: float or int ?

        """
        # annual grow of the fadder
        self.available_fodder['Herbivore'] = self.parameters['f_max']

    @staticmethod
    def set_given_parameters(given_parameters):
        """
        Sets the user defined parameters that applies to Jungle.

        Parameters
        ----------
        given_parameters: dict
        """
        for parameter in given_parameters:
            if parameter in Jungle.parameters:
                Jungle.parameters[parameter] = \
                    given_parameters[parameter]
            else:
                # unknown parameter
                raise RuntimeError('Unknown parameter, ' +
                                   str(parameter) +
                                   ' can\'t be set')


class Desert(Landscape):
    """
    Animals may stay in the desert, but there is no fodder available to
    herbivores there. Carnivores can prey on herbivores in the desert.
    """
    is_accessible = True
    available_fodder = {'Herbivore': 0}

    def __init__(self):
        super().__init__()

        # self.available_fodder['Herbivore'] = 0
        total_herb_weight = sum(
            i.weight for i in self._in_cell_fauna['Herbivore'])
        self.available_fodder['Carnivore'] = total_herb_weight
        self.available_fodder['Herbivore'] = Desert.available_fodder[
            'Herbivore']
        # should we move aviable_fodder to the class level
        # That's because it's not changeable, so it's private variable


class Mountain(Landscape):
    """
    The mountain can not be entered by animals. So that the animal lists are
    always empty for this kind of landscape and there is no fodder.
    """
    available_fodder = {'Herbivore': 0, 'Carnivore': 0}
    in_cell_fauna = {'Herbivore': [], 'Carnivore': []}
    is_accessible = False

    # That's because it's not changeable, so it's private variable, fixed
    # class variabels for all classes

    def __init__(self):
        # if fauna_objects_dict is not None:
        #    raise ValueError('Animals can\'t be set on Mountains, '
        #                     'this parameter has to be empty')
        super().__init__()
        self.available_fodder = Mountain.available_fodder
        self.in_cell_fauna = Mountain.in_cell_fauna


class Ocean(Landscape):
    """
    The ocean can not be entered by animals. So that the animal lists are
    always empty for this kind of landscape and there is no fodder.
    """
    available_fodder = {'Herbivore': 0, 'Carnivore': 0}
    in_cell_fauna = {'Herbivore': [], 'Carnivore': []}
    is_accessible = False

    # That's because it's not changeable, so it's private variable
    # those are instance variables becuase they are fixed for all
    # instances of the class, meaning if those value changes, they will
    # chnaged in all instances of the variables
    def __init__(self):
        super().__init__()
        # if in_cell_fauna is not None:
        #    raise ValueError('Animals can\'t be set on Ocean, '
        #                     'this parameter has to be empty')
        self.available_fodder = Ocean.available_fodder
        self._in_cell_fauna = Ocean.in_cell_fauna
        # overwrite the object fauna_objects_list to be equals to empty list,
        # is that right?


if __name__  == '__main__':
    s = Savannah()
    h1 = Herbivore()
    c1 = Carnivore()
    s.add_animal(h1)
    s.add_animal(c1)
    print(s._in_cell_fauna)
    for species in s._in_cell_fauna:
        print(s._in_cell_fauna[species])

    dict_ = {Herbivore: h1, Carnivore: c1}
    for ele in dict_:
        print(ele)
        print(dict_[ele])