# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

import math
from biosim.fauna import Herbivore, Carnivore
import operator
import numpy as np
from random import seed


class Landscape:
    available_fodder = {}
    parameters = {}

    def __init__(self, in_cell_fauna):
        # those fauna list is given from the map, which was given earlier
        # from the simulation as initial animals and we append it to when
        # migration and birthing
        self.in_cell_fauna = in_cell_fauna
        # that should be list of dicts
        self.sorted_fauna_fitness = {}

    def save_fitness(self, fauna_objects, species):
        # this is to update the current fitness to be able to use in
        # the order later
        # remember also that fitness is goijg to change each time they eat
        species_fauna_fitness = {}
        # saving the data only for the species that we want to save,
        # not for all
        for fauna in fauna_objects[species]:
            species_fauna_fitness[fauna] = fauna.fitness
        self.sorted_fauna_fitness[species] = species_fauna_fitness

    def sort_by_fitness(self, animal_objects, species, reverse=True):
        self.save_fitness(animal_objects, species)
        if reverse:
            self.sorted_fauna_fitness[species] = dict(
                sorted(self.sorted_fauna_fitness[species].items(),
                       key=operator.itemgetter(1), reverse=True))
        else:
            self.sorted_fauna_fitness[species] = dict(
                sorted(self.sorted_fauna_fitness[species].items(),
                       key=operator.itemgetter(1)))
        # all fitnesses is sorted for the animals in species, depends on the
        # parameters whether it should be sorted or reverse sorted

    def relevant_fodder(self, animal, cell):
        # This is f_k
        species = animal.__class__.__name__
        return cell.available_fodder[species]
        # remember each time a carni move, number of herbi is
        # differnt in the cells, since they travel based on fitness
        # maybe a herbi is higher fitness

    def relative_abundance_fodder(self, animal, dist_cell):
        key = animal.__class__.__name__
        return self.relevant_fodder(animal, dist_cell) / (
                (len(self.in_cell_fauna[key]) + 1) *
                animal.parameters['F'])
        # we instantiate object of teh species given and get F from it
        # maybe there is error here

    def propensity(self, animal, dist_cell):
        if dist_cell.__class__.__name__ in ['Mountain', 'Ocean']:
            return 0
        else:
            relevant_fodder = self.relative_abundance_fodder(animal, dist_cell)
            return math.exp(relevant_fodder * animal.parameters['lambda'])
            # need to fix this spcies(), we need an object to be able to access
            # parameters

    def add_fauna(self, animal):
        key = animal.__class__.__name__
        self.in_cell_fauna[key].append(animal)

    def remove_fauna(self, animal):
        key = animal.__class__.__name__
        self.in_cell_fauna[key].remove(animal)

    def mate(self, fauna_object):
        # now change the population of the cell
        # decrease the weight of the mother
        species = fauna_object.__class__
        num_fauna = len(self.in_cell_fauna[species.__name__])
        if np.random.random() > fauna_object.birth_probablity(num_fauna):
            # if that random number is bigger than that probablity it should
            # give birth, or create new baby, or object of animal
            baby = species()
            if fauna_object.weight < baby.parameters['w_birth'] * \
                    baby.parameters['xi']:
                # it gives birth only if its weight is more than the the
                # weight to be losed
                self.add_fauna(baby)
                fauna_object.give_birth(baby)
                # that's still wrong becuase it's with the weight of the baby
            else:
                pass
                # dont give birth ?

    def feed_herbivore(self):
        # that should return the amount of food that is going to be
        # eaten by all animals in celll
        self.sort_by_fitness(self.in_cell_fauna, 'Herbivore')
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
            if herb_available_fodder == 0:
                break
                # break the for-loop to save computation cost becuase it's no
                # longer effective to iterate through it and they will not
                # recieve any food
                # Animals here recieves no food
                # self._available_fodder = 0
                # last else statment is not required, so we can remove it and add
                # it to the elif
            elif herb_available_fodder >= herbivore.parameters['F']:
                # animals eat what he required
                amount_to_eat = herbivore.parameters['F']
                herbivore.eat(amount_to_eat)
                self.available_fodder['Herbivore'] -= amount_to_eat
            elif 0 < herb_available_fodder < herbivore.parameters['F']:
                # animals eat what is left
                amount_to_eat = self.available_fodder['Herbivore']
                herbivore.eat(amount_to_eat)
                self.available_fodder['Herbivore'] = 0

    def feed_carnivore(self):
        self.sort_by_fitness(self.in_cell_fauna, 'Carnivore')
        self.sort_by_fitness(self.in_cell_fauna, 'Herbivore', False)
        # reverse order the carnivore by fitness and sort the herbivore
        for carnivore in self.sorted_fauna_fitness['Carnivore']:
            # carbivore with highest fitness will kill the lowest fitness
            # herbivore first and so on
            if len(self.sorted_fauna_fitness['Herbivore']) > 0:
                # if available food (weight of herbi) is zero ,break the for loop becuase it's
                # no longer efficient
                for herbivore in self.sorted_fauna_fitness['Herbivore']:
                    # carnivore will kill herivore as a time
                    # if the
                    if np.random.random() > carnivore.kill_probablity(
                            herbivore):
                        weight_to_eat = herbivore.weight
                        # del self.sorted_fauna_fitness['Herbivore'][herbivore]
                        # remove it from the dictionary, meaning removing from the cell
                        # herbivore.die()
                        # we need a good implimenetation for method die in the fauna
                        if weight_to_eat >= carnivore.parameters['F']:
                            # that's wrong becuase, the weight to eat is the weight
                            # of only one meal
                            carnivore.eat(carnivore.parameters['F'])
                        elif weight_to_eat < carnivore.parameters['F']:
                            carnivore.eat(weight_to_eat)


class Savannah(Landscape):
    is_accessible = True
    parameters = {'f_max': 300.0, 'alpha': 0.3}

    def __init__(self, in_cell_fauna, given_parameters=None):
        super().__init__(in_cell_fauna)
        if given_parameters is not None:
            self.set_given_parameters(given_parameters)
        self.parameters = Savannah.parameters
        self.available_fodder['Herbivore'] = self.parameters['f_max']
        total_herb_weight = sum(i.weight for i in
                                self.in_cell_fauna['Herbivore'])
        self.available_fodder['Carnivore'] = total_herb_weight
        # aviable fodder equals to f_max at the beginning of
        # instaniating anew object

    def grow_fodder(self):
        # annual grow of the fodder
        self.available_fodder['Herbivore'] += self.parameters['alpha'] \
                                              * (self.parameters['f_max']
                                                 - self.available_fodder[
                                                     'Herbivore'])

    @staticmethod
    def set_given_parameters(given_parameters):
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
    is_accessible = True
    parameters = {'f_max': 300.0}

    def __init__(self, fauna_objects_dict, given_parameters=None):
        super().__init__(fauna_objects_dict)
        if given_parameters is not None:
            self.set_given_parameters(given_parameters)
        self.parameters = Jungle.parameters
        self.available_fodder['Herbivore'] = self.parameters['f_max']
        total_herb_weight = sum(
            i.weight for i in self.in_cell_fauna['Herbivore'])
        self.available_fodder['Carnivore'] = total_herb_weight
        # amount of initial fodder aviable should equals to f_max

    def grow_herb_fodder(self):
        # annual grow of the fadder
        self.available_fodder['Herbivore'] = self.parameters['f_max']

    @staticmethod
    def set_given_parameters(given_parameters):
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
    is_accessible = True
    available_fodder = {'Herbivore': 0}

    def __init__(self, in_cell_fauna):
        super().__init__(in_cell_fauna)

        self.in_cell_fauna = in_cell_fauna
        # self.available_fodder['Herbivore'] = 0
        total_herb_weight = sum(
            i.weight for i in self.in_cell_fauna['Herbivore'])
        self.available_fodder['Carnivore'] = total_herb_weight
        self.available_fodder['Herbivore'] = Desert.available_fodder['Herbivore']
        # should we move aviable_fodder to the class level
        # That's because it's not changeable, so it's private variable


class Mountain(Landscape):
    available_fodder = {'Herbivore': 0, 'Carnivore': 0}
    in_cell_fauna = {'Hernivore': [], 'Carnivore': []}
    is_accessible = False

    # That's because it's not changeable, so it's private variable, fixed
    # class variabels for all classes

    def __init__(self, fauna_objects_dict=None):
        if fauna_objects_dict is not None:
            raise ValueError('Animals can\'t be set on Mountains, '
                             'this parameter has to be empty')
        super().__init__(fauna_objects_dict)
        self.available_fodder = Mountain.available_fodder
        self.in_cell_fauna = Mountain.in_cell_fauna


class Ocean(Landscape):
    available_fodder = {'Herbivore': 0, 'Carnivore': 0}
    in_cell_fauna = {'Hernivore': [], 'Carnivore': []}
    is_accessible = False

    # That's because it's not changeable, so it's private variable
    # those are instance variables becuase they are fixed for all
    # instances of the class, meaning if those value changes, they will
    # chnaged in all instances of the variables
    def __init__(self, in_cell_fauna=None):
        super().__init__(in_cell_fauna)
        if in_cell_fauna is not None:
            raise ValueError('Animals can\'t be set on Ocean, '
                             'this parameter has to be empty')
        self.available_fodder = Ocean.available_fodder
        self.in_cell_fauna = Ocean.in_cell_fauna
        # overwrite the object fauna_objects_list to be equals to empty list,
        # is that right?


if __name__ == '__main__':
    h1 = Herbivore()
    h2 = Herbivore()
    c1 = Carnivore()
    c2 = Carnivore()
    animals = {'Carnivore': [c1, c2], 'Herbivore': [h1, h2]}
    s = Savannah(animals)
    print(s.available_fodder)
    o = Ocean()
    print(o)
