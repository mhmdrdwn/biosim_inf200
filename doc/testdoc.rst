Tests
======
This project is written in a test driven methodology. Unit tests are written for testing the functionality of software.
The concepts of fixtures are used. Also, the statistical tests and some compatibility checks and acceptance tests are added.


Classes
--------
The tests consists of these python files.

* **test_fauna.py**: contains *Fauna* abstract class and its subclasses, *Herbivore* and *Carnivore*.
* **test_landscapes.py**: consists of *Landscape* abstract class and its subclasses, *Savannah*, *Jungle*, *Desert*, *Mountain* and *Ocean*.
* **test_map.py**: has *Map* class.
* **test_simulation.py**: contains *BioSim* class.
* **test_visualisation.py**: has *Visualisation* class.
* **test_statistical.py**: statistic test for testing the distribution is added.

Also, two compatibility checks are provided by EPAP, and the biosim package passes both:

* **test_biosim-interface.py**
* **check_sim.py**


.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Contents:

   test_faunadoc
   test_landscapesdoc
   test_mapdoc
   test_simulationdoc
   test_visualisationdoc
   test_statisticaldoc
