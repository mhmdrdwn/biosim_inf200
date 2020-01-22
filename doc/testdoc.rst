Tests
======
This project is written in a test driven view. Unit tests are written for designing and testing the functionality of software.
Also, the concepts of fixtures are used. Moreover, the statistical tests and some compatibility checks and acceptance tests are added.


Test Classes
------------
The tests consists of these python files.

* **test_fauna.py**: contains unit tests in *TestFauna*, *TestHerbivores* and *TestCarnivores* classes.
* **test_landscapes.py**: consists of unit tests in *TestLandscapes*, *TestOcean*  *TestDesert*, *TestMountains*, *TestSavannah* and *TestJungle* classes.
* **test_map.py**: has unit tests in *TestMap* class.
* **test_statistical.py**: consists of statistical test *TestGaussian* and *TestProbability* classes.

Also, biosim package passes the two compatibility checks provided by EPAP:

* **test_biosim-interface.py**
* **check_sim.py**


.. toctree::
   :maxdepth: 2
   :titlesonly:
   :caption: Contents:

   test_faunadoc
   test_landscapesdoc
   test_mapdoc
   test_statisticaldoc
   test_visualisationdoc
