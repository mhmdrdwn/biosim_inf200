# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Mohamed Radwan, Nasibeh Mohammadi'
__email__ = 'mohamed.radwan@nmbu.no, nasibeh.mohammadi@nmbu.no'

from biosim.simulation import BioSim
import matplotlib.pyplot as plt


class VisualizeMovie:
    def __init__(self):
        pass

    def visual_movie(self):
        """
        This is a small demo script running a ranvis simulation and generating a movie.
        """
        island_map =
        sim = BioSim((10, 15), 0.1, 12345, '../BIOSIM')
        sim.simulate(100, 1, 5)
        sim.make_movie('mp4')
        sim.make_movie('gif')

if __name__ == '__main__':
    """
    This is a small demo script running a ranvis simulation.
    """

    sim = img_base((10, 15), 0.1, 12345)
    sim.simulate(50, 1, 5)

    input('Press ENTER to simulate some more!')

    sim.simulate(100, 1, 5)

    print('Close the figure to end the program!')

    plt.show()

