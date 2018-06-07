"""
Created by Kieran Bates

the agent that fires projectiles on user command
"""

from graphics import egi, KEY
from vector2d import Vector2D
from projectile import Projectile


class Cannon(object):
    GUN_MODES = {
        KEY._1: 'rifle',
        KEY._2: 'rocket',
        KEY._3: 'hand_gun',
        KEY._4: 'grenade'
    }

    def __init__(self, pos, world=None, angle=90.0, scale=30.0, mass=1.0, mode='rifle'):
        self.pos = pos
        self.world = world
        self.mode = mode
        self.angle = angle
        self.mass = mass
        self.scale = Vector2D(scale, scale)
        self.heading = Vector2D(90, 90)
        self.side = self.heading.perp()
        self.max_speed = 20.0 * scale
        self.colour = 'RED'

    def render(self):
        egi.set_pen_color(name=self.colour)
        egi.circle(self.pos, 10)

    # -------------------------------------------------------------------------------------------

    def fire(self):
        """fires a projectile"""
        print("fired: " + self.mode)
        self.world.projectiles.append(Projectile(self.mode, self.pos.copy(), 30.0, self.world))
