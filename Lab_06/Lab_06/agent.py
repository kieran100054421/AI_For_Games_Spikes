'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path

AGENT_MODES = {
    KEY._1: 'seek',
    KEY._2: 'arrive_slow',
    KEY._3: 'arrive_normal',
    KEY._4: 'arrive_fast',
    KEY._5: 'flee',
    KEY._6: 'pursuit',
    KEY._7: 'follow_path',
    KEY._8: 'wander'
}


class Agent(object):
    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        'normal': 0.6,
        'fast': 0.3
    }

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='seek'):
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

        # Wander info
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 1.0 * scale
        self.wander_radius = 1.0 * scale
        self.wander_jitter = 10.0 * scale
        self.bRadius = scale

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
        self.path = Path()
        self.waypoint_threshold = 10.0
        self.randomise_path()

    def calculate(self, delta):
        # reset the steering force
        mode = self.mode
        if mode == 'seek':
            accel = self.seek(self.world.target)
        elif mode == 'arrive_slow':
            accel = self.arrive(self.world.target, 'slow')
        elif mode == 'arrive_normal':
            accel = self.arrive(self.world.target, 'normal')
        elif mode == 'arrive_fast':
            accel = self.arrive(self.world.target, 'fast')
        elif mode == 'flee':
            accel = self.flee(self.world.target)
        elif mode == 'follow_path':
            accel = self.follow_path(self.path)
        elif mode == 'wander':
            accel = self.wander(delta)
        ##        elif mode == 'pursuit':
        ##            accel = self.pursuit(self.world.hunter)
        else:
            accel = Vector2D()
        self.acceleration = accel

        return accel

    def update(self, delta):
        ''' update vehicle position and orientation '''
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
        ''' Draw the triangle agent with color'''
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)

        # draw wander info
        if self.mode == 'wander':
            # calculate the center of the wander circle in front of the agent
            wnd_pos = Vector2D(self.wander_dist, 0)
            wnd_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
            # draw wander circle
            egi.green_pen()
            egi.circle(wnd_pos, self.wander_radius)
            # draw the wander target (little cirlce on the big circle)
            egi.red_pen()
            wnd_pos = (self.wander_target + Vector2D(self.wander_dist, 0))
            wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
            egi.circle(wld_pos, 3)

        if self.mode == 'follow_path':
            self.path.render()

        # draw it!
        egi.closed_shape(pts)

    def speed(self):
        return self.vel.length()

    # --------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def flee(self, hunter_pos):
        ''' move away from hunter position '''
        ## add panic distance (second)
        ## add flee calculations (first)
        panic_range_sq = 10000

        if self.pos.distanceSq(hunter_pos) > panic_range_sq:
            return Vector2D()

        desired_vel = (self.pos - hunter_pos).normalise() * self.max_speed

        return (desired_vel - self.vel)

    def arrive(self, target_pos, speed):
        ''' this behaviour is similar to seek() but it attempts to arrive at
            the target position with a zero velocity'''
        decel_rate = self.DECELERATION_SPEEDS[speed]
        to_target = target_pos - self.pos
        dist = to_target.length()

        if dist > 0:
            # calculate the speed required to reach the target given the
            # desired deceleration rate
            speed = dist / decel_rate
            # make sure the velocity does not exceed the max
            speed = min(speed, self.max_speed)
            # from here proceed just like Seek except we don't need to
            # normalize the to_target vector because we have already gone to the
            # trouble of calculating its length for dist.
            desired_vel = to_target * (speed / dist)
            return (desired_vel - self.vel)

        return Vector2D(0, 0)

    def pursuit(self, evader):
        ''' this behaviour predicts where an agent will be in time T and seeks
            towards that point to intercept it. '''
        ## OPTIONAL EXTRA... pursuit (you'll need something to pursue!)
        return Vector2D()

    def randomise_path(self):
        '''creates a randomised path for the agent to follow'''
        cx = self.world.cx  # width
        cy = self.world.cy  # height
        min_x = self.world.cx - cx + 1  # min width
        min_y = self.world.cy - cy + 1  # min height
        margin = min(cx, cy) * (1 / 6)  # use this for padding in the next liner
        # self.path.create_random_path(self.waypoint_threshold, margin, margin, cx, cy)
        self.path.create_random_path(self.waypoint_threshold, 100, 100, cx - margin, cy - margin, True)

    def follow_path(self, path):
        '''follows a path by going to each node in the path'''
        # if the path has finished arrive slowly at the current point
        # otherwise check if distance is within threshold and if is include
        # the current point. Seek the current point
        if path.is_finished():
            return self.arrive(path.current_pt(), 'slow')
        else:
            if self.waypoint_threshold > self.pos.distance(path.current_pt()):
                path.inc_current_pt()

            return self.seek(path.current_pt())

    def wander(self, delta):
        """random wandering using projected jitter circle"""
        wt = self.wander_target
        # this behaviour is dependant on the update rate, so this line must
        # be included when using time independant frame rate
        jitter_tts = self.wander_jitter * delta
        # first, add a small random vector to the targets position
        wt += Vector2D(uniform(-1, 1) * jitter_tts, uniform(-1, 1) * jitter_tts)
        # re-project this new vector back on to a unit circle
        wt.normalise()
        # increase the length of the vector to the same radius
        # of the wander circle
        wt *= self.wander_radius
        # move the target into a position WonderDist in front of the agent
        target = wt + Vector2D(self.wander_dist, 0)
        # project the target into world space
        wld_target = self.world.transform_point(target, self.pos, self.heading, self.side)

        return self.seek(wld_target)
