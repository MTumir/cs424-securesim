#!/usr/bin/python3

import time
import random
import argparse
import logging

from attacks.replay_attack import ReplayAttack

logger = logging.getLogger(__name__)
from process_sim.temperature_control import TemperatureControl
from control_logic.tc_controller import TC_Controller
from attacks.false_data_injection import FalseDataInjection
from attacks.dos_attack import DoSAttack

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-de', help='0=no debug messages, 1=debug messages', action='store_true')
    parser.add_argument('--injection', '-i', help='1=activate injection attacks', action='store_true')
    parser.add_argument('--dos', '-d', help='1=activate DoS attacks', action='store_true')
    parser.add_argument('--replay', '-r', help='1=activate replay attacks', action='store_true')
    
    args = parser.parse_args()
    if (args.debug == 0):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

    tc = TemperatureControl(low_bound=40.0, high_bound=50.0)
    controller = TC_Controller(tc)
    injection = FalseDataInjection(tc)
    dos = DoSAttack(tc)
    replay = ReplayAttack(tc)

    if (args.injection == 1):
        injection.activate()
    if (args.dos == 1):
        dos.activate()
    if (args.replay == 1):
        replay.activate()

    tc.start_simulation()
    controller.start_control()

    try:
        for _ in range(2000):
            randint = random.randint(1,10)

            # Execute attacks randomly
            if (randint % 2 == 0):
                injection.attack()
            if (randint >= 5):
                dos.attack()
            if (randint <= 6):
                 replay.attack()

            temp = tc.get_temperature()
            logger.info(f"Temperature: {temp:.2f}°C | Change Rate: {tc.temp_change:.2f}°C/s")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping simulation...")
    finally:
        tc.stop_simulation()
        controller.stop_control()

if __name__ == "__main__":
    main()