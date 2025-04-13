#!/usr/bin/python3

import random
import logging
logger = logging.getLogger(__name__)

class FalseDataInjection:
    def __init__(self, tc):
        self.active = False
        self.tc = tc

    def attack(self):        
        if not self.active:
            return

        if (bool(random.getrandbits(1))):
            direction = "Decreasing"
            new_bound = round(self.tc.low_bound - random.random(), 1)
        else:
            direction = "Increasing"
            new_bound = round(self.tc.low_bound + random.random(), 1)
            if new_bound > self.tc.high_bound:
                new_bound = self.tc.high_bound
        
        logger.warning(f'\t{direction} low_bound from {self.tc.low_bound} to {new_bound}')
        self.tc.low_bound = new_bound

    def activate(self):
        self.active = True