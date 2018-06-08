from random import choice

class Rando(object):
    """description of class"""

    def update(self, gameinfo):
        # only send one fleet at a time
        if gameinfo.my_fleets:
            return

        # check if we should attack
        if gameinfo.my_planets and gameinfo.not_my_planets:
            # select random target and destination

            dest = list()
            src = list()

            # have all planets with that have 100 or more ships attack
            for p in gameinfo.my_planets:
                #dest.add(max(f.not_my_planets.values(), key = lambda p: 1.0 / (1 + p.num_ships)))
                #src.add(max(f.my_planets.values(), key = lambda p: p.num_ships))
                dest.append(p.not_my_planets.values())
                src.append(p.my_planets.values())


            intAverage = int(float(len(dest) + len(src)) / 2)

            for i in range(0, intAverage, 1): 
                if src[i].num_ships > 10:
                    gameinfo.planet_order(src[i], dest[i], int(src[i].num_ships * 0.75))
            # launch new fleet if there's enough
            #if src.num_ships > 10:
            #    gameinfo.planet_order(src, dest, int(src.num_ships * 0.75))