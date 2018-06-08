class Simple(object):

    def update(self, gameinfo):
        """updates the bot according to the weakest planet"""

        if gameinfo.my_fleets:
            return

        if gameinfo.my_planets and gameinfo.not_my_planets:
            dest = max(gameinfo.not_my_planets.values(), key=lambda p: p.num_ships)
            src = max(gameinfo.my_planets.values(), key=lambda p: p.num_ships)

            if src.num_ships > 10:
                gameinfo.planet_order(src, dest, int(src.num_ships * 0.75))
