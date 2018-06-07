"""
Created by Kieran Bates

This class acts as an agent travelling to the destination
"""

from graphics import egi
from point2d import Point2D


class Agent(object):
    def __init__(self):
        self.radius = 7.5
        self.colour = 'PURPLE'
        self.pos = None
        self.path = []

    def update_path(self, path):
        """updates the agents path"""
        if path is not self.path:
            self.path = path
            self.pos = 0

    def update(self):
        """updates the agents location"""
        if self.pos != len(self.path) - 1:
            self.pos += 1
