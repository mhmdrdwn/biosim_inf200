# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

import math

from biosim.fauna import Fauna
from biosim.fauna import Herbivore
from biosim.fauna import Carnivore
import operator
import numpy as np

class Landscapes:
    def __init__(self, fauna_objects_dict):
        self._available_fodder = 0
        # those fauna list is given from the map, which was given earlier
        # from the simulation as initial animals and we append it to when
        # migration and birthing
        self.fauna_objects_dict = fauna_objects_dict
        # that should be list of dicts
        self.sorted_fauna_fitness = {}

    def save_fitness(self, fauna_objects, species):
        # this is to update the current fitness to be able to use in
        # the order later
        # remember also that fitness is goijg to change each time they eat
        species_fauna_fitness = {}
        # saving the data only for the species that we want to save, not for all
        for fauna in fauna_objects[species]:
            species_fauna_fitness[fauna] = fauna.fitness
        self.sorted_fauna_fitness[species] = species_fauna_fitness

    def order_by_fitness(self, to_sort_objects, species, reverse = True):
        self.save_fitness(to_sort_objects, species)
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

    def calculate_relative_abundance_fodder(self, species):
        return self.relevant_fodder(species)/((len(self.fauna_objects_dict[species])+1)*species().parameters['F'])
        # we instantiate object of teh species given and get F from it
        # maybe there is error here

    def relevant_fodder(self, species):
        if species == 'Herbivore':
            return self._available_fodder
            # return amount of relevant fodder for the differnt animals species
        elif species == 'Carnivore':
            total_herbi_weight = 0
            for herbivore in self.fauna_objects_dict['Herbivore']:
                total_herbi_weight += herbivore.weight
            return total_herbi_weight
            # remember each time a carni move, number of herbi is
            # differnt in the cells, since they travel based on fitness
            # maybe a herbi is higher fitness

    def propensity(self, species, cell):
        if cell == 'Mountain' or j == 'Ocean':
            return 0
        elif j is None:
            relevant_fodder = self.calculate_relative_abundance_fodder(species)
            return math.exp(relevant_fodder*species().parameters['lambda'])
            # need to fix this spcies(), we need an object to be able to access
            # parameters

    def probability(self, species, cell, adj_cells):
        total_propensity = 0
        for cell in adj_cells:
            total_propensity += self.propensity(species, cell)
        return self.propensity(species, cell)/total_propensity
        # this is the rule of probablity
        if species().parameters['lambda'] == 0:
            # all possible distination will be cjosen with equal probablity
        elif species().parameters['lambda'] == 0:
            # animals will go to cell with greater abundance of food
        else:
            # animals will turn away from food

    def herbivore_eat(self):
        # that should return the amount of food that is going to be
        # eaten by all animals in celll
        self.order_by_fitness(self.fauna_objects_dict, 'Herbivore')
        # we need to sort animals by fitness prior to the eating, and the
        # animals with highest fitness eats first
        for herbivore in self.sorted_fauna_fitness['Herbivore']:
            # this is already reverse sorted dictionary, so animals at the
            # beginning are the hight fitness
            # heribore is an object that is saved in the dictionary,
            # eat method is amethod in Fauna class
            # change the amount of avialable fadder in landscape after animal eats
            # eaten_food = 0

            if self._available_fodder == 0:
                break
                # break the for-loop to save computation cost becuase it's no
                # longer effective to iterate through it and they will not
                # recieve any food
                # Animals here recieves no food
                # self._available_fodder = 0
                # last else statment is not required, so we can remove it and add
                # it to the elif
            elif self._available_fodder >= herbivore.parameters['F']:
                # animals eat what he required
                amount_to_eat = herbivore.parameters['F']
                herbivore.eat(amount_to_eat)
                self._available_fodder -= amount_to_eat
            elif 0 < self._available_fodder < herbivore.parameters['F']:
                # aniamls eats what is left
                amount_to_eat = self._available_fodder
                herbivore.eat(amount_to_eat)
                self._available_fodder = 0

    def carnivore_eat(self):
        self.order_by_fitness(self.fauna_objects_dict, 'Carnivore')
        self.order_by_fitness(self.fauna_objects_dict, 'Herbivore', False)
        #reverse order the carnivore by fitness and sort the herbivore
        for carnivore in self.sorted_fauna_fitness['Carnivore']:
            # carbivore with highest fitness will kill the lowest fitness
            # herbivore first and so on
            if len(self.sorted_fauna_fitness['Herbivore']) == 0:
                break
                #if avaiable food (weight of herbi) is zero ,break the for loop becuase it's
                # no longer efficient
            for herbivore in self.sorted_fauna_fitness['Herbivore']:
                # carnivore will kill herivore as a time
                # if the
                carnivore.calculate_killing_probablity(herbivore.fitness)
                if np.random.random() > carnivore.killing_probablity:
                    weight_to_eat = herbivore.weight
                    #del self.sorted_fauna_fitness['Herbivore'][herbivore]
                    # remove it from the dictionary, meaning removing from the cell
                    #herbivore.die()
                    # we need a good implimenetation for method die in the fauna
                    if weight_to_eat >= carnivore.parameters['F']:
                        # that's wrong becuase, the weight to eat is the weight
                        # of only one meal
                        carnivore.eat(carnivore.parameters['F'])
                    elif weight_to_eat < carnivore.parameters['F']:
                        carnivore.eat(weight_to_eat)
                        
    @property
    def available_fodder(self):
        return self._available_fodder
    # why that???


class Savannah(Landscapes):
    is_accessible = True

    def __init__(self, fauna_objects_dict):
        super().__init__(fauna_objects_dict)
        self.alpha = 0.3
        self.f_max = 300
        self._available_fodder = self.f_max
        # aviable fodder equals to f_max at the beginning of
        # instaniating anew object

    def grow_fodder(self):
        # annual grow of the fodder
        self._available_fodder += self.alpha * (self.f_max -
                                                self._available_fodder)


class Jungle(Landscapes):
    is_accessible = True

    def __init__(self, fauna_objects_dict):
        super().__init__(fauna_objects_dict)
        self.f_max = 800
        self._available_fodder = self.f_max
        # amount of initial fodder aviable should equals to f_max

    def grow_fodder(self):
        # annual grow of the fadder
        self._available_fodder = self.f_max


class Desert(Landscapes):
    is_accessible = True
    available_fodder = 0

    def __init__(self, fauna_objects_list):
        super().__init__(fauna_objects_list)
        self._available_fodder = Desert.available_fodder
        # should we move aviable_fodder to the class level

        # That's because it's not changeable, so it's private variable


class Mountain(Landscapes):
    available_fodder = 0
    fauna_objects_dict = {}
    is_accessible = False

    # That's because it's not changeable, so it's private variable, fixed
    # class variabels for all classes

    def __init__(self, fauna_objects_dict):
        super().__init__(fauna_objects_dict)
        self.available_fodder = Mountain.available_fodder


class Ocean(Landscapes):
    available_fodder = 0
    fauna_objects_dict = {}
    is_accessible = False

    # That's because it's not changeable, so it's private variable
    # those are instance variables becuase they are fixed for all
    # instances of the class, meaning if those value changes, they will
    # chnaged in all instances of the variables
    def __init__(self, fauna_objects_dict):
        super().__init__(fauna_objects_dict)
        self.fauna_objects_list = Ocean.fauna_objects_dict
        # overwrite the object fauna_objects_list to be equals to empty list,
        # is that right?


# testing
h1 = Herbivore()
h1.fitness = 10
h2 = Herbivore()
h2.fitness = 20
c1 = Carnivore()
c1.fitness = 10
c2 = Carnivore()
c2.fitness = 20
animals = {'Carnivore': [c1, c2], 'Herbivore': [h1, h2]}
s = Savannah(animals)
print(s.fauna_objects_dict)
print(s.available_fodder)
s.grow_fodder()
print(s.available_fodder)
# s.reduce_fodder(10)
print(s.available_fodder)
# print(s.herbivore())
s.order_by_fitness(animals, 'Herbivore', False)
s.order_by_fitness(animals, 'Carnivore')
s.herbivore_eat()
s.carnivore_eat()
print(s.sorted_fauna_fitness)
print('###########')
j = Jungle(animals)
print(j.fauna_objects_dict)
print(j.available_fodder)
j.grow_fodder()
print(j.available_fodder)
print('###########')
o = Ocean(animals)
print("ocean " + str(o.fauna_objects_list))
print(o.available_fodder)
d = Desert(animals)
# d.grow_fodder_annual()
print(d.available_fodder)
print('###########')
print(d.fauna_objects_dict)
print(d.available_fodder)
print('###########')
m = Mountain(animals)
print(m.fauna_objects_dict)
print(m.available_fodder)
