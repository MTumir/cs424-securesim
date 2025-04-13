#!/usr/bin/python3

import time
import random
from process_sim.temperature_control import TemperatureControl
from control_logic.tc_controller import TC_Controller
from attacks.false_data_injection import FalseDataInjection

def main():
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
            print(f"Temperature: {temp:.2f}°C | Change Rate: {tc.temp_change:.2f}°C/s")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping simulation...")
    finally:
        tc.stop_simulation()
        controller.stop_control()

if __name__ == "__main__":
    main()