from random import choice


class Complex(object):

    def __init__(self):
        self.enemy_planets = []
        self.pos_dest = []
        self.previous = None

    def update_enemy_ships(self, gameinfo):
        """updates the list of enemy ships according to gameinfo"""
        for planet in self.enemy_planets:
            found = False

            for key in gameinfo.my_planets:
                if planet.id == gameinfo.my_planets[key].id:
                    found = True

            if not found:
                self.enemy_planets.remove(planet)

        for k in gameinfo.enemy_planets:
            found = False

            for planet in self.enemy_planets:
                if gameinfo.enemy_planets[k].id == planet.id:
                    if gameinfo.enemy_planets[k].num_ships < planet.num_ships:
                        self.pos_dest.append(gameinfo.enemy_planets[k])

                    planet.num_ships = gameinfo.enemy_planets[k].num_ships
                    found = True

            if not found:
                self.enemy_planets.append(gameinfo.enemy_planets[k].copy())

    def update(self, gameinfo):
        """updates the bot according to the enemy planet that just fired ships"""
        self.pos_dest.clear()

        if len(self.enemy_planets) == 0:
            for k in gameinfo.enemy_planets:
                self.enemy_planets.append(gameinfo.enemy_planets[k].copy())
                self.pos_dest.append((gameinfo.enemy_planets[k]))
        else:
            self.update_enemy_ships(gameinfo)

        if gameinfo.my_fleets:
            return

        if gameinfo.my_planets or gameinfo.not_my_planets:
            if len(self.pos_dest) == 0:
                dest = self.enemy_planets[0]
            elif len(self.pos_dest) == 1:
                dest = self.pos_dest[0]
            else:
                dest = choice(self.pos_dest)

            if dest == self.previous:
                dest = min(gameinfo.not_my_planets.values(), key=lambda p: p.num_ships)

            if len(gameinfo.my_planets) > 0:
                src = max(gameinfo.my_planets.values(), key=lambda p: p.num_ships)
            else:
                src = None  # = min(gameinfo.my_planets.values(), key=lambda p: p.num_ships)

            if dest is None:
                for key in gameinfo.my_planets:
                    if gameinfo.my_planets[key].id == self.previous.id:
                        pass
                dest = self.previous
            if src is None:
                pass
            elif src.num_ships > dest.num_ships:
                gameinfo.planet_order(src, dest, int(src.num_ships * 0.75))
                self.previous = dest
