"""
An obstacle for agents to hide behind

Created by Kieran Bates
"""

from graphics import egi
from vector2d import Vector2D
from random import randrange


class Obstacle(object):
    def __init__(self,  x, y,):
        self.pos = Vector2D(randrange(x), randrange(y))
        self.radius = 30.0
        self.color = 'WHITE'
        self.border_radius = self.radius * 1.5

    def render(self):
        """renders the obstacle on the screen"""
        egi.set_pen_color(name=self.color)
        egi.circle(self.pos, self.radius, True)
