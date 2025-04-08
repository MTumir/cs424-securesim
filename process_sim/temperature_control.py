#!/usr/bin/python3

import threading
import time
import random

class TemperatureControl:
    def __init__(self, low_bound, high_bound):
        self.low_bound = low_bound
        self.high_bound = high_bound
        self.temperature = 35.0  # Start below low_bound to test controller
        self.temp_change = 0.0
        self.running = True
        self.natural_drift = -0.2  # Natural cooling rate

    def update(self):
        while self.running:
            noise = random.uniform(-0.1, 0.1)
            self.temperature += self.natural_drift + self.temp_change + noise
            self.temperature = max(0.0, min(100.0, self.temperature))
            time.sleep(1)

    def start_simulation(self):
        thread = threading.Thread(target=self.update)
        thread.start()

    def stop_simulation(self):
        self.running = False

    def set_temp_change(self, change):
        self.temp_change = change

    def get_temperature(self):
        return self.temperature