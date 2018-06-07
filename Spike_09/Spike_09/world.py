'''A 2d world that supports agents with steering behaviour

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''
from Hunter import Hunter
from vector2d import Vector2D
from matrix33 import Matrix33
from graphics import egi
from projectile import Projectile


class World(object):
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.target = Vector2D(cx / 2, cy / 2)
        self.hunter = None
        self.paused = True
        self.showinfo = True
        self.cannon = None
        self.projectiles = []

    def update(self, delta):
        if not self.paused:
            if self.hunter.moving:
                self.hunter.update(delta)

            for i in range(len(self.projectiles) - 1):
                self.projectiles[i].update(delta)

                if self.projectiles[i].out_of_bounds() or self.collision(self.projectiles[i]) \
                        or self.projectiles[i].target_reached():
                    delete = self.projectiles[i]
                    self.projectiles.remove(self.projectiles[i])
                    self.delete_projectile(delete)

    def render(self):
        self.hunter.render()
        self.cannon.render()

        for projectile in self.projectiles:
            projectile.render()

        if self.target:
            egi.red_pen()
            egi.cross(self.target, 10)

        if self.showinfo:
            infotext = ', '.join(set(projectile.mode for projectile in self.projectiles))
            egi.white_pen()
            egi.text_at_pos(0, 0, infotext)

    def wrap_around(self, pos):
        ''' Treat world as a toroidal space. Updates parameter object pos '''
        max_x, max_y = self.cx, self.cy
        if pos.x > max_x:
            pos.x = pos.x - max_x
        elif pos.x < 0:
            pos.x = max_x - pos.x
        if pos.y > max_y:
            pos.y = pos.y - max_y
        elif pos.y < 0:
            pos.y = max_y - pos.y

    def transform_point(self, point, pos, forward, side):
        """Transform the given single point using the provided position,
            and direction (foward and side unit vectors), to object world space"""
        # make a copy of original point (so we don't trash them)
        wld_pt = point.copy()
        # create a transformation matrix to perform the operations
        mat = Matrix33()
        # rotate
        mat.rotate_by_vectors_update(forward, side)
        # and translate
        mat.translate_update(pos.x, pos.y)
        # now transform the point (in place)
        mat.transform_vector2d(wld_pt)

        return wld_pt


    def transform_points(self, points, pos, forward, side, scale):
        ''' Transform the given list of points, using the provided position,
            direction and scale, to object world space. '''
        # make a copy of original points (so we don't trash them)
        wld_pts = [pt.copy() for pt in points]
        # create a transformation matrix to perform the operations
        mat = Matrix33()
        # scale,
        mat.scale_update(scale.x, scale.y)
        # rotate
        mat.rotate_by_vectors_update(forward, side)
        # and translate
        mat.translate_update(pos.x, pos.y)
        # now transform all the points (vertices)
        mat.transform_vector2d_list(wld_pts)
        # done
        return wld_pts

    def delete_projectile(self, projectile):
        """deletes a projectile"""
        del projectile

    def collision(self, projectile):
        """detects whether a projectile has collided with the hunter"""
        # print(self.hunter.pos.distance_sq(projectile.pos))

        if self.hunter.pos.distance_sq(projectile.pos) < 75:
            return True
        else:
            return False
