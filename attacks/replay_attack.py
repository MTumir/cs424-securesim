import logging
import threading
import time
from random import random, randint

from process_sim.temperature_control import TemperatureControl

logger = logging.getLogger(__name__)

class ReplayAttack:
    def __init__(self, tc):
        self.active = False
        self.tc = tc

    def attack(self):
        if not self.active:
            return

        #initial setup variables
        data = self.tc.temperature
        delay = randint(1, 10)

        #creates a new message for each iteration
        timestamp = str(time.time())
        msg = f'{data} at {timestamp}'

        logger.debug(f'Current Temperature is: {msg}')

        #Captures temperature and sets temperature to the captured value
        logger.debug(f'Attacker captures message: {msg}')

        start_time = time.perf_counter()
        while time.perf_counter() - start_time < delay:
            pass
        logger.info(f'Changing temperature to: {msg}')
        self.tc.temperature = data

    def activate(self):
        self.active = True
        logger.info(f'Replay Attack activated')

    def deactivate(self):
        self.active = False