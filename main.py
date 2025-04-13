#!/usr/bin/python3

import time
import random
import argparse
import logging
logger = logging.getLogger(__name__)
from process_sim.temperature_control import TemperatureControl
from control_logic.tc_controller import TC_Controller
from attacks.false_data_injection import FalseDataInjection

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', help='0=no debug messages, 1=debug messages', type=int, default=0)
    
    args = parser.parse_args()
    if (args.debug == 0):
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)

    tc = TemperatureControl(low_bound=40.0, high_bound=50.0)
    controller = TC_Controller(tc)
    injection = FalseDataInjection(tc)

    tc.start_simulation()
    controller.start_control()

    try:
        for _ in range(2000):
            randint = random.randint(1,10)

            # Execute attacks randomly
            if (randint % 2 == 0):
                injection.attack()
            # if (randint >= 5):
                # DOS attack
            # if (randint <= 6):
                # Replay attack

            temp = tc.get_temperature()
            logger.info(f"\tTemperature: {temp:.2f}°C | Change Rate: {tc.temp_change:.2f}°C/s")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping simulation...")
    finally:
        tc.stop_simulation()
        controller.stop_control()

if __name__ == "__main__":
    main()