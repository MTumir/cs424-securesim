#!/usr/bin/python3

import unittest

# Add root directory to the import path
import sys
sys.path.insert(0, '')
from process_sim.temperature_control import TemperatureControl

class Test_TemperatureControl(unittest.TestCase):

    def setUp(self):
        self.tc = TemperatureControl(low_bound=40.0, high_bound=50.0)

    def test_init(self):
        print('\tRunning test_init')
        self.assertEqual(self.tc.low_bound, 40.0)
        self.assertEqual(self.tc.high_bound, 50.0)
        self.assertEqual(self.tc.temperature, 35.0)
        self.assertEqual(self.tc.temp_change, 0.0)
        self.assertEqual(self.tc.running, True)
        self.assertEqual(self.tc.natural_drift, -0.2)

    def test_stop_simulation(self):
        print('\tRunning test_stop_simulation')
        self.assertEqual(self.tc.running, True)
        self.tc.stop_simulation()
        self.assertEqual(self.tc.running, False)

    def test_set_temp_change(self):
        print('\tRunning test_set_temp_change')
        self.assertEqual(self.tc.temp_change, 0.0)
        self.tc.set_temp_change(3.0)
        self.assertEqual(self.tc.temp_change, 3.0)

    def test_get_temperature(self):
        print('\tRunning test_get_temperature')
        self.assertEqual(self.tc.temperature, self.tc.get_temperature())        

if __name__ == '__main__':
    unittest.main()