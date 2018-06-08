"""
Created by Kieran Bates

This class represents the world and controls everything in it.
"""

from need import Need
from agent import Agent
from action import Action
import os


class World(object):
    def __init__(self, agent, time=0):
        self.max_time = time + 720
        self.start_time = 480 + time
        self.current_time = time
        self.play = True
        self.agent = agent
        self.writes = []

    def update(self):
        """updates the world and its contents"""
        self.agent.update(1)

        self.current_time += 1

        if self.current_time == self.max_time or not self.agent.alive:
            self.play = False

    def render(self):
        """Renders the world and its contents"""
        border = "\n----------------------------------------"
        hours, minutes = self.calculate_time()
        out = border

        if minutes < 10:
            out += "\nTIME: " + str(hours) + ":0" + str(minutes)
        else:
            out += "\nTIME: " + str(hours) + ":" + str(minutes)
        out += "\nTIME: " + str(self.current_time)
        out += "\n" + self.agent.render()

        print(out)
        self.writes.append(out)

    def to_file(self):
        """writes all display messages to a file"""

        # delete file if exists
        try:
            os.remove("./log/log.txt")
        except OSError:
            pass

        # write all outputs to file
        with open("./log/log.txt", "a") as out_file:
            for write in self.writes:
                out_file.write(write)
        out_file.close()

    def calculate_time(self):
        """calculates the time in hours and minutes"""
        hours = 0
        count = 0
        time = self.current_time + self.start_time

        for i in range(time):
            if count == 60:
                hours += 1
                count = 0

            count += 1

        minutes = count

        return hours, minutes
