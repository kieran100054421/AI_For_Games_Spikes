"""
Created by Kieran Bates

This class plans a list of actions for the agent to undertake according to the agents needs
"""

from sys import maxsize


class Planner(object):
    def __init__(self, actions, agent=None, limit=3):
        self.agent = agent
        self._actions = actions     # list of all actions
        self.plan = []              # list of planned actions
        self._limit = limit         # the limit of goals
        self.goals = {}             # dictionary of the lowest needs

    def change_name(self):
        """Changes the phrase 'the agent' in each of the actions to the name specified by the user"""
        if self.agent and self.agent.name != "Agent":
            for action in self._actions:
                split = action.description.split()
                if split[0] == "The" and split[1] == "agent":
                    action.description.replace("The agent", self.agent.name)

    def best_goals(self):
        """gets the 3 best goals"""
        lowest_value = []
        lowest_name = []

        for i in range(self._limit):
            lowest_value.append(float("inf"))
            lowest_name.append("")

        for need in self.agent.needs:
            if need.value < lowest_value[0]:
                lowest_value[2] = lowest_value[1]
                lowest_name[2] = lowest_name[1]
                lowest_value[1] = lowest_value[0]
                lowest_name[1] = lowest_name[0]
                lowest_value[0] = need.value
                lowest_name[0] = need.name
            elif need.value < lowest_value[1]:
                lowest_value[2] = lowest_value[1]
                lowest_name[2] = lowest_name[1]
                lowest_value[1] = need.value
                lowest_name[1] = need.name
            elif need.value < lowest_value[2]:
                lowest_value[2] = need.value
                lowest_name[2] = need.name

        index = self._limit

        while index < len(lowest_value):
            del lowest_value[index]
            del lowest_name[index]
            index += 1

        for i in range(self._limit):
            self.goals[lowest_name[i]] = lowest_value[i]

    def best_action(self, key, value):
        """finds the best action that positively addresses the need"""
        pos_actions = []    # list of all possible actions

        # get all actions that have a positive affect on the need
        for action in self._actions:
            if key in action.need_modifiers and action.need_modifiers[key] > 0.0 and action.priority == 2:
                if action.complete is True and action.repeatable is True:
                    pos_actions.append(action)
                elif action.complete is False:
                    pos_actions.append(action)

        best_action = None
        highest_value = float("inf")

        # find the best action amongst all possible actions
        for need in self.agent.needs:
            if key == need.name:
                if value <= need.warning_point:
                    # if the needs value is less then or equal to the warning point search for the action
                    # with the highest value and lowest time
                    lowest_time = maxsize
                    for action in pos_actions:
                        if action.time_taken < lowest_time and action.need_modifiers[need.name] < highest_value:
                            best_action = action
                            lowest_time = action.time_taken
                            highest_value = action.need_modifiers[need.name]
                break

        for action in pos_actions:
            if action.need_modifiers[key] < highest_value:
                best_action = action
                highest_value = action.need_modifiers[key]

        best_action.complete = False

        return best_action

    def priority_one(self, actions):
        """checks for priority one actions"""
        for need in self.agent.needs:
            if need.value == 0.0 and need.zero_time < 15:
                goals_keys = []
                goals_values = []

                for key, value in self.goals.items():
                    goals_keys.append(key)
                    goals_values.append(value)

                self.goals.clear()

                if len(goals_keys) == 2:
                    print()
                msg = "Values length (" + str(len(goals_values)) + ") does not equal keys length (" + \
                      str(len(goals_keys)) + ") or goals list does not equal 3 (" + str(len(goals_keys)) + ")"
                assert len(goals_values) == len(goals_keys) and len(goals_keys) == 3, msg

                if need.name not in goals_keys:
                    goals_values[2] = goals_values[1]
                    goals_keys[2] = goals_keys[1]
                    goals_values[1] = goals_values[0]
                    goals_keys[1] = goals_keys[0]
                    goals_values[0] = need.value
                    goals_keys[0] = need.name

                index = 0

                while index < self._limit:
                    self.goals[goals_keys[index]] = goals_values[index]
                    index += 1

                assert len(self.goals) == 3, "goals length not 3: " + str(self.goals) + " " + str(goals_keys) + \
                                             " " + str(goals_values)

                for action in self._actions:
                    if action.priority == 1 and need.name in action.need_modifiers and \
                            action.need_modifiers[need.name] > 0.0:
                        self.remove_last(actions)
                        actions.append(action)

    def remove_last(self, actions):
        """removes the last element of actions"""
        index = 0
        for action in actions:
            if index == len(actions) - 1:
                actions.remove(action)

            index += 1

    def plan_actions(self):
        """plans the most appropriate actions"""
        actions = []
        self.goals.clear()
        self.plan.clear()

        if self.agent.action.name == "Play Computer Games" and \
                self.agent.time_passed - self.agent.action.time_taken == -1:
            print()

        self.best_goals()

        for key, value in self.goals.items():
            actions.append(self.best_action(key, value))

        self.priority_one(actions)

        # check if the agent's hunger, thirst, energy or boredom needs are at 0 and at the zero time
        if (self.agent.needs[0].value == 0 and self.agent.needs[0].zero_time == 15) or\
                (self.agent.needs[1].value == 0 and self.agent.needs[1].zero_time == 15) or\
                (self.agent.needs[5].value == 0 and self.agent.needs[5].zero_time == 15):
            for action in self._actions:
                if action.name == "Death":
                    actions[2] = actions[1]
                    actions[1] = actions[0]
                    actions[0] = action

                    break

        # sort by highest priority
        actions.sort(key=lambda a: a.priority)

        for action in actions:
            self.plan.append(action)

    def render(self):
        """renders the goals formulated by the planner"""
        out = "{"
        for key in self.goals:
            out += key + ": " + str(self.goals[key]) + " "
        out += "}"

        return out
