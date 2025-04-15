#!/usr/bin/python3

import threading
import time
import logging
logger = logging.getLogger(__name__)

class TC_Controller:
    def __init__(self, tc):
        self.tc = tc
        self.running = True

    def control_loop(self):
        while self.running:
            temperature = self.tc.get_temperature()
            if temperature < self.tc.low_bound:
                logger.debug(f"Temp {temperature:.2f}°C < {self.tc.low_bound}°C, heating")
                self.tc.set_temp_change(0.5)
            elif temperature > self.tc.high_bound:
                logger.debug(f"Temp {temperature:.2f}°C > {self.tc.high_bound}°C, cooling")
                self.tc.set_temp_change(-0.5)
            else:
                logger.debug(f"Temp {temperature:.2f}°C in range, stabilizing")
                self.tc.set_temp_change(0.0)
            time.sleep(1)

    def start_control(self):
        thread = threading.Thread(target=self.control_loop)
        thread.start()

    def stop_control(self):
        self.running = False