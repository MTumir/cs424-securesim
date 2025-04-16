import logging
from random import randint

from process_sim.temperature_control import TemperatureControl

logger = logging.getLogger(__name__)

class ReplayAttack:
    def __init__(self, tc):
        self.active = False
        self.tc = tc
        self.data = 0.0
        self.delay = randint(1,5)

    def attack(self):
        if not self.active:
            return

        # Grab new data if none is held
        if (self.data == 0.0):
            self.data = round(self.tc.temperature, 2)

        # Debug statement stating data and remaining delay
        logger.debug(f'Attacker has temperature: {self.data}, delay is {self.delay}')

        # If delay isn't up, decrement delay
        if (self.delay != 0):
            self.delay -= 1
        # Otherwise overwrite temperature with stored data
        else:
            logger.info(f'Changing temperature to: {self.data}')
            self.tc.temperature = self.data
            self.data = 0.0
            self.delay = randint(1,5)

    def activate(self):
        self.active = True
        logger.info(f'Replay Attack activated')

    def deactivate(self):
        self.active = False