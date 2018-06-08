"""
Created by Kieran Bates

This class represents an action that the agent can take
"""


class Action(object):
    # initialises an action object. The name is the name of the action
    # time taken is the time it takes to
    def __init__(self, name, time_taken, priority, repeatable, description, needs, modifiers):
        self.name = name                    # the actions name
        self.time_taken = time_taken        # the time taken to complete the action
        self.priority = priority            # the priority of the action. the higher the number the lower the priority
        self.description = description      # a description of the task
        self.need_modifiers = {}            # the needs changed by this action
        self.repeatable = repeatable        # whether the action can be
        self.complete = False               # whether the action has been completed or not. If a prerequisite

        assert (len(needs) == len(modifiers)), "amount of needs has to be the same as amount of modifiers"
        i = 0

        while i < (len(needs) + len(modifiers)) / 2:
            self.need_modifiers[needs[i]] = modifiers[i]
            i += 1
