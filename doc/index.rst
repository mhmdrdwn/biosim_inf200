.. Modeling documentation master file, created by
   sphinx-quickstart on Thu Jan 16 10:31:54 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Modelling the Ecosystem of Rossum Island.
=========================================
Project in Advance Programming at Realtek / NMBU, January 2020

Mohamed Radwan, Nasibeh Mohammadi

What is BioSim
--------------
BioSim is a project that simulates animal population of
an island - Rossum island - for many years. This project is
developed for Environmental Protection Agency of Pylandia.
EAPA wants to study the stability of the ecosystem of island to
preserve the island as a nature park for future generation.
The ecosystem is simulated under the object-oriented programming
concepts written in Python programming language (python 3.6).

The Ecosystem
--------------
Rossum island cosists of several different landscapes which are as
follows:

* **Jungle**: provides large amount of fodder even under intense grazing.
* **Savannah**: provides a limited amount of fodder.
* **Desert**: does not provide fodder for herbivores.
* **Mountain**: is impassable for animals.
* **Ocean**: like mountains is impassable for animal. Also, the edges of the island are surrounded by ocean.

In addition, on the island two species of animal live:

* **Herbivores**: depend on a good supply of fodder to survive and reproduce.
* **Carnivores**: depend on the availability of prey. They are more more mobile than herbivores.

Simulation
----------
The software allows user to observe long term behaviour of ecosystem by changing the
input variables. The characteristics of fauna like aging, birth, death and fitness are
shown in plots. Moreover, animals can migrate from a region to another one for food. They
can move to one of the four neighbouring cells but not diagonal cells.

Annual Cycle
------------
The stages of annual cycle on the island are supposed as the seasons on Rossum island which are:
#. **Feeding**:
#. **Breeding**: When calculating the probability of birth according to equation
the number of animals at the start of the breeding season is used, new born animals
do not count.
#. **Migration**: Animals can migrate at most once per year.
#. **Aging**: Each animal becomes one year older.
#. **Loss of weight**: All animals lose weight each year.
#. **Death**:


.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Contents:

   classdoc
   testdoc

References
----------
.. [Ref] Yngve Mardal Moe. Modelling the Ecosystem of Rossum Island. Version 2019.1: 2019-01-03.




Indices
========

* :ref:`genindex`
* :ref:`modindex`
