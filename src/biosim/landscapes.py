# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from biosim.fauna import Fauna
from biosim.fauna import Herbivore
from biosim.fauna import Carnivore
import operator


class Landscapes:
    def __init__(self, fauna_objects_dict):
        self._available_fodder = 0
        # those fauna list is given from the map, which was given earlier
        # from the simulation as initial animals and we append it to when
        # migration and birthing
        self.fauna_objects_dict = fauna_objects_dict
        # that should be list of dicts
        self.fauna_fitness = {}

    def save_fitness(self, fauna_objects, species):
        # this is to update the current fitness to be able to use in
        # the order later
        # remember also that fitness is goijg to change each time they eat
        species_fauna_fitness = {}
        # saving the data only for the species that we want to save, not for all
        for fauna in fauna_objects[species]:
            species_fauna_fitness[fauna] = fauna.fitness
        self.fauna_fitness[species] = species_fauna_fitness

    def order_by_fitness(self, to_sort_objects, species):
        self.save_fitness(to_sort_objects, species)
        self.fauna_fitness[species] = dict(
            sorted(self.fauna_fitness[species].items(),
                   key=operator.itemgetter(1), reverse=True))
        # all fitnesses is sorted for the animals in species

    def herbivore(self):
        # that should return the amount of food that is going to be
        # eaten by all animals in celll
        self.order_by_fitness(self.fauna_objects_dict['Herbivore'])
        # we need to sort animals by fitness prior to the eating, and the
        # animals with highest fitness eats first
        for fauna in self.fauna_objects_dict['']:
            reverse_sorted_fitness = sorted(fauna.fitness)

    def reduce_fodder(self, amount_to_reduce):
        # change the amount of avialable fadder in landscape after animal eats
        # eaten_food = 0
        if self._available_fodder >= amount_to_reduce:
            # animals eat what he required
            self._available_fodder -= amount_to_reduce
        elif 0 < self._available_fodder < amount_to_reduce:
            # aniamls eats what is left
            self._available_fodder = 0
        else:
            # animals here recieves no food
            self._available_fodder = 0
        # last else statment is not required, so we can remove it and add
        # it to the elif

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
s.reduce_fodder(10)
print(s.available_fodder)
# print(s.herbivore())
s.order_by_fitness(animals, 'Herbivore')
s.order_by_fitness(animals, 'Carnivore')

print(s.fauna_fitness)
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
