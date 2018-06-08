"""
Created by Kieran Bates

This class represents a need that an agent has
"""


class Need(object):
    def __init__(self, name, value=10.0, warning_point=3.0, decay_at=30, decay_amount=0.5):
        self.value = value
        self.name = name
        self.warning_point = warning_point
        self.decay_at = decay_at
        self.decay_amount = decay_amount
        self.decay_time = 0
        self.max = 10.0
        self.min = 0.0
        self.zero_time = 0
        self.message = ""

    def update(self, time=0.0, value=0.0):
        """updates the current need"""
        self.decay_time += time

        # update the value
        self.value += value

        if self.value == 0.0:
            self.zero_time += time
        else:
            self.zero_time = 0

        # check if decay time has reached decay at reset decay time and subtract
        # decay amount from the value
        if self.decay_time == self.decay_at:
            self.decay_time = 0
            self.value -= self.decay_amount

        # update value if out of bounds to the closest bound
        if self.value < self.min:
            self.value = self.min
        if self.value > self.max:
            self.value = self.max

        # check if warning point has been reached and if has set message for retrieval
        if self.value < self.warning_point:
            self.message = "Agent's " + self.name + " needs to be taken care of"
        else:
            self.message = ""
