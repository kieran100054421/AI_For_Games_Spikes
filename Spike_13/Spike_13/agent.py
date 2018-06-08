"""
Created by Kieran Bates
Date: 2/06/2018

Represents an agent
"""

from need import Need
from random import choice


class Agent(object):
    def __init__(self, planner, action, name="Agent"):
        self.name = name
        self.planner = planner
        self.plan = planner.plan
        self.action = action
        self.time_passed = 0
        self.alive = True
        self.messages = []
        self.needs = [
            Need("HUNGER"),
            Need("THIRST"),
            Need("BLADDER"),
            Need("BOREDOM"),
            Need("HYGIENE"),
            Need("ENERGY")
        ]  # end self.needs

        self.planner.change_name()

    def update(self, time):
        """updates the agent"""
        self.plan.clear()
        self.time_passed += time

        # update each of the needs
        for need in self.needs:
            need.update(time)
            if need.message != "":
                self.messages.append(need.message)

        # plan actions
        self.planner.plan_actions()
        self.plan = self.planner.plan

        # check if action has completed and if has update needs and choose new action
        if self.time_passed == self.action.time_taken:
            self.messages.append(self.name + " has completed action: " + self.action.name)
            self.messages.append(self.action.description)
            if self.action.name == "Death":
                self.alive = False
            for need in self.needs:
                for key in self.action.need_modifiers:
                    if need.name == key:
                        need.update(time, self.action.need_modifiers[key])
                        if need.message != "":
                            self.messages.append(need.message)
            self.planner.plan_actions()
            self.plan = self.planner.plan
            self.action = self.plan[0]
            self.time_passed = 0

        # update action
        for action in self.plan:
            if action.priority == 1 and self.action.priority == 2:
                self.messages.append(self.name + " stopped " + self.action.name + " to " + action.name)
                self.action = action
                self.time_passed = 0
            if action.priority == 0:
                self.messages.append(self.name + " stopped " + self.action.name + " to " + action.name)
                self.action = action
                self.alive = False
                self.time_passed = 0

    def render(self):
        """displays the state of the agent and all messages"""
        # render each of the needs
        out = "NEEDS: { "
        for need in self.needs:
            out += need.name + ": " + str(need.value) + ", "
        out += "}\n"

        # render the current action
        time_left = self.time_passed - self.action.time_taken
        out += "CURRENT ACTION: " + self.action.name + ": COMPLETION TIME:" + str(self.action.time_taken) + \
               " TIME LEFT: " + str(time_left)

        out += "\nGOALS: " + self.planner.render()

        out += "\nPLANNED ACTIONS: ["
        for action in self.plan:
            out += "NAME: " + action.name + " PRIORITY: " + str(action.priority) + " MODIFIERS: {"
            for key in action.need_modifiers:
                out += key + ": " + str(action.need_modifiers[key]) + " "
            out += "}, "
        out += "]"

        out += "\nMESSAGES: ["
        for message in self.messages:
            out += "\n\t" + message
        out += "\n]"

        self.messages.clear()

        return out
