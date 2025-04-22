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
        
        # Generate a value to alter low_bound by between 0 and 1.
        adjust = round(random.random(), 1)
        while (adjust == 0.0):
            adjust = round(random.random(), 1)
        logger.debug(f'Adjusting low_bound by {adjust}')

        # 50% chance to decrease low_bound by adjust
        if (bool(random.getrandbits(1))):
            direction = "Decreasing"
            new_bound = round(self.tc.low_bound - adjust, 1)
        # 50% chance to increase low_bound by adjust
        else:
            direction = "Increasing"
            new_bound = round(self.tc.low_bound + adjust, 1)
            # Cap low_bound at high_bound
            if new_bound > self.tc.high_bound:
                new_bound = self.tc.high_bound
        
        logger.warning(f'{direction} low_bound from {self.tc.low_bound} to {new_bound}')
        self.tc.low_bound = new_bound

    def activate(self):
        self.active = True
        logger.info(f'False data injection attack activated')

    def deactivate(self):
        self.active = False