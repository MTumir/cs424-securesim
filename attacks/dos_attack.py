#!/usr/bin/python3

import random
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
        requests = random.randint(10, 50) # Random number of requests per attack cycle 
        self.request_count += requests

        # Log the attack
        logger.warning(f'\tSending {requests} requests to system')

        # Simulate the system overload
        if self.request_count > self.max_requests:
            logger.critical(f'\tSystem overloaded with {self.request_count} requests')
        #simulate response time increase due to overload from requests
            self.tc.response_time = max(0.1, self.tc.response_time * 1.1)
            logger.warning(f'\tResponse time increased to {self.tc.response_time:.2f}s')


        #reset request count 
        if random.random() < 0.1:
            self.request_count = 0
            logger.info(f'\tRequest count reset')
        
    def activate(self):
        self.active = True
        logger.info(f'\tDoS attack activated')

    def deactivate(self):
        self.active = False