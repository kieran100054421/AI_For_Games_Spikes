'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians, sqrt
from random import random, randrange

AGENT_MODES = {
        KEY._1: 'flee',
        KEY._2: 'hide'
}


class Agent(object):
    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        'normal': 0.6,
        'fast': 0.3
    }

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='flee'):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        # where am i and where am i going? random
        dir = radians(random() * 360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.acceleration = Vector2D()  # current steering force
        self.mass = mass

        # limits?
        self.max_speed = 20.0 * scale
        self.max_force = 500.0
        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0, 0.6),
            Point2D(1.0, 0.0),
            Point2D(-1.0, -0.6)
        ]

        self.detect_width = 1.0
        self.min_detect_length = 50.0
        self.hide_locations = []

    def calculate(self, delta):
        # reset the steering force
        mode = self.mode
        if mode == 'flee':
            self.world.hunter.set_visible(True)
            accel = self.flee()
        elif mode == 'hide':
            accel = self.hide()
        else:
            accel = Vector2D()
        self.acceleration = accel

        return accel

    def update(self, delta):
        """ update vehicle position and orientation """
        acceleration = self.calculate(delta)
        # new velocity
        self.vel += acceleration * delta
        # check for limits of new velocity
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta
        # update heading is non-zero velocity (moving)
        if self.vel.length_sq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()

        # treat world as continuous space - wrap new position if needed
        self.world.wrap_around(self.pos)
        force = self.calculate(delta)
        force.truncate(self.max_force)

    def render(self, color=None):
        """ Draw the triangle agent with color"""
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)

        # draw it!
        egi.closed_shape(pts)

        # display each possible hiding location
        for spot in self.hide_locations:
            if spot == self.hide_locations[-1]:
                egi.set_pen_color(name='GREEN')
            egi.cross(spot, 10)

    def speed(self):
        return self.vel.length()

    # --------------------------------------------------------------------------

    def flee(self):
        """move away from hunter position"""
        panic_range_sq = 1000
        if self.pos.distance(self.world.hunter.pos) > panic_range_sq:
            return Vector2D()

        desired_vel = (self.pos - self.world.hunter.pos).normalise() * self.max_speed

        return (desired_vel - self.vel)

    def arrive(self, speed, best_spot=None):
        """ this behaviour is similar to seek() but it attempts to arrive at
            the target position with a zero velocity"""
        decel_rate = self.DECELERATION_SPEEDS[speed]
        dist = best_spot.length()

        if dist > 0:
            # calculate the speed required to reach the target given the
            # desired deceleration rate
            speed = dist / decel_rate
            # make sure the velocity does not exceed the max
            speed = min(speed, self.max_speed)
            # from here proceed just like Seek except we don't need to
            # normalize the to_target vector because we have already gone to the
            # trouble of calculating its length for dist.
            desired_vel = best_spot * (speed / dist)

            return (desired_vel - self.vel)

        return Vector2D(0, 0)

    # def interpose(self):
    #     """finds the midpoint between the agent and hunter"""
    #     # estimate the time to arrive at mid point
    #     mid_point = (self.pos + self.world.hunter.pos) / 2.0
    #     eta = self.pos.distance(mid_point) / self.max_speed
    #
    #     # predict future position of self and hunter at time T
    #     posA = self.pos + self.world.hunter.vel * eta
    #     posB = self.world.hunter.pos + self.world.hunter.vel * eta
    #     # predict future mid point
    #     mid_point = (posA + posB) / 2.0
    #
    #     return self.arrive(mid_point)

    def get_hiding_position(self, obstacle):
        """find available hiding spots for given obstacle"""
        dist_from_boundary = 30.0
        dist_away = obstacle.radius + dist_from_boundary
        to_obstacle = (obstacle.pos - self.world.hunter.pos).normalise()

        return (to_obstacle * dist_away) + obstacle.pos

    def hide(self):
        """hides the agent from hunters"""
        dist_closest = float('inf')
        best_spot = None
        self.hide_locations.clear()

        # check for possible hiding spots
        for obstacle in self.world.obstacles:
            hiding_spot = self.get_hiding_position(obstacle)
            hiding_dist = hiding_spot.distance_sq(self.pos)

            if hiding_dist < dist_closest:
                self.hide_locations.append(hiding_spot)
                dist_closest = hiding_dist
                best_spot = hiding_spot

        # if we have a best hiding spot, use it
        if best_spot:
            return self.arrive('fast', best_spot)

        # run away!
        return self.flee()
