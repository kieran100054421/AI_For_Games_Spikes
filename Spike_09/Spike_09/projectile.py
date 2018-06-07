"""
Created by Kieran Bates

acts a projectile that been shot
"""
from typing import Dict, List

from graphics import egi
from math import sin, cos, radians
from vector2d import Vector2D
from random import random, randrange


class Projectile(object):
    # projectile mode: speed: accuracy
    PROJECTILE_MODES = {
        'rifle': [0.3, 0.8],
        'rocket': [0.8, 0.8],
        'hand_gun': [0.3, 0.3],
        'grenade': [0.8, 0.3]
    }

    def __init__(self, mode, pos, scale=30.0, world=None, radius=7.5):
        self.mode = mode
        self.world = world
        dir = radians(random() * 360)
        self.pos = pos
        self.target = Vector2D()
        self.radius = radius
        self.vel = Vector2D()
        # self.vel = Vector2D() * (PROJECTILE_MODES[self.mode][0] * 10)
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.colour = 'WHITE'
        self.speed = self.PROJECTILE_MODES[mode][0] * 10
        self.scale = Vector2D(scale, scale)
        self.acceleration = Vector2D()
        self.max_speed = 20.0 * scale
        self.max_force = 500.0
        self.turn_rate = 1.0
        self.updates = 0

        # self.vel = self.interpose()

    def calculate(self, delta):
        mode = self.mode

        if self.updates == 0:
            accel = self.interpose()
        else:
            if mode in self.PROJECTILE_MODES:
                accel = self.arrive()
            else:
                accel = Vector2D()

        self.acceleration = accel
        self.updates += 1

        return accel

    def out_of_bounds(self):
        """check if projectiles is within bounds"""
        if self.pos.x >= self.world.cx or self.pos.y >= self.world.cy:
            return True
        else:
            return False

    def target_reached(self):
        """Checks if projectile has reached its target"""
        if self.pos.x >= self.target.x or self.pos.y >= self.target.y:
            print("Target Reached")
            return True
        else:
            return False

    def update(self, delta):
        # self.pos += self.vel

        acceleration = self.calculate(delta)
        # new velocity
        self.vel += acceleration * delta
        # check for limits of the new velocity
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta
        if self.pos == self.target:
            self.world.projectiles.remove(self)
        # update heading is non-zero velocity (moving)
        if self.vel.length_sq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
        # treat world as continuous space
        self.world.wrap_around(self.pos)
        force = self.calculate(delta)
        force.truncate(self.max_force)

    def render(self):
        egi.set_pen_color(name=self.colour)
        egi.circle(self.pos, self.radius, True)
        egi.set_pen_color(name='YELLOW')
        egi.cross(self.target, 10.0)

    # ========================================================================
    def seek(self, target_pos):
        """moves towards the target position"""
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed

        return desired_vel - self.vel

    def arrive(self):
        """moves the projectile towards the target"""
        decel_rate = self.PROJECTILE_MODES[self.mode][0]
        to_target = self.target - self.pos
        dist = to_target.length()

        if dist > 0:
            speed = dist / decel_rate
            speed = min(speed, self.max_speed)
            desired_vel = to_target * (speed / dist)
            return (desired_vel - self.vel)

    def pursuit(self):
        """predicts the location that the hunter will be"""
        to_evader = self.world.hunter.pos - self.pos

        # time relative to distance, inversly proportional to sum of velocities
        look_ahead_time = to_evader.length() / (self.max_speed + self.world.hunter.speed())
        # turn rate delay? dot product
        look_ahead_time += (1 - self.heading.dot(self.world.hunter))* -self.turn_rate
        # seek the predicted location (using look-ahead time)
        look_ahead_pos = self.world.hunter.pos + self.world.hunter.vel * look_ahead_time

        return self.seek(look_ahead_pos)

    def interpose(self):
        """estimates the location of the hunter"""
        mid_point = (self.pos + self.world.hunter.pos) / 2.0
        eta = self.pos.distance(mid_point) / self.max_speed

        posA = self.pos + self.vel * eta
        posB = self.world.hunter.pos + self.world.hunter.vel * eta

        i = randrange(1, 10)
        print(i)

        if i < self.PROJECTILE_MODES[self.mode][1] * 10:
            self.target = (posA + posB) / 2
        else:
            self.target = posB

        return self.arrive()

