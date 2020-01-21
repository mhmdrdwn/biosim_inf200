Implementation
====================
The BioSim is modelled after the ``scikit-learn`` API
and should be fully compliant with the ``scikit-learn`` ecosystem.
Consequently, it depends on ``numpy``, ``scipy``
and ``scikit-learn``.

Classes
--------
This project consists of five python files. Each file contains classes and subclasses.

* **fauna.py**: contains *Fauna* abstract class and its subclasses, *Herbivore* and *Carnivore*.
* **landscapes.py**: consists of *Landscape* abstract class and its subclasses, *Savannah*, *Jungle*, *Desert*, *Mountain* and *Ocean*.
* **map.py**: has *Map* class.
* **simulation.py**: contains *BioSim* class.
* **visualisation.py**: has *Visualisation* class.

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Contents:

   faunadoc
   landscapesdoc
   mapdoc
   simulationdoc
   visualisationdoc
