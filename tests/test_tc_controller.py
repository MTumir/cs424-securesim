#!/usr/bin/python3

import unittest
import time

# Add root directory to the import path
import sys
sys.path.insert(0, '')
from process_sim.temperature_control import TemperatureControl
from control_logic.tc_controller import TC_Controller

class Test_TC_Controller(unittest.TestCase):

    def setUp(self):
        tc = TemperatureControl(low_bound=40.0, high_bound=50.0)
        self.controller = TC_Controller(tc)

    def test_init(self):
        print('\tRunning test_init')
        tc = TemperatureControl(low_bound=40.0, high_bound=50.0)

        # Check if self.controller.tc was created properly
        self.assertEqual(self.controller.tc.low_bound, tc.low_bound)
        self.assertEqual(self.controller.tc.high_bound, tc.high_bound)
        self.assertEqual(self.controller.tc.temperature, tc.temperature)
        self.assertEqual(self.controller.tc.temp_change, tc.temp_change)
        self.assertEqual(self.controller.tc.running, tc.running)
        self.assertEqual(self.controller.tc.natural_drift, tc.natural_drift)

        self.assertEqual(self.controller.running, True)

    def test_control_loop(self):
        print('\tRunning test_control_loop')
        start_temp = self.controller.tc.temperature
        self.assertEqual(start_temp, 35)
        self.controller.tc.start_simulation()
        self.controller.start_control()
        time.sleep(1)
        self.controller.tc.stop_simulation()
        self.controller.stop_control()
        self.assertNotEqual(start_temp, self.controller.tc.temperature)
        
    def test_stop_control(self):
        print('\tRunning test_stop_control')
        self.assertEqual(self.controller.running, True)
        self.controller.stop_control()
        self.assertEqual(self.controller.running, False)   

if __name__ == '__main__':
    unittest.main()