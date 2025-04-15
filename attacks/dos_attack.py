#!/usr/bin/python3

import random
import time
import logging
from logging import getLogger

logger = getLogger(__name__)

class DoSAttack:
    def __init__(self, tc):
        self.active = False
        self.tc = tc
        self.request_count = 0
        self.max_requests = 1000 # Max number of requests to simulate

    def attack(self):
        if not self.active:
            return
        #incoming requests
        requests = random.randint(100, 300) # Random number of requests per attack cycle 
        self.request_count += requests

        # Log the attack
        logger.warning(f'Sending {requests} requests to system')

        # Simulate the system overload
        if self.request_count > self.max_requests:
            logger.critical(f'System overloaded with {self.request_count} requests')
        #simulate response time increase due to overload from requests
            time.sleep(0.003 * self.request_count)
            if random.random() < 0.3:
                self.clearRequestCount()


        #randomly reset request count 
        if random.random() < 0.1:
            self.clearRequestCount()

    def clearRequestCount(self):
        self.request_count = 0
        logger.info(f'Request count reset')
        
    def activate(self):
        self.active = True
        logger.info(f'DoS attack activated')

    def deactivate(self):
        self.active = False