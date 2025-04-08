#!/usr/bin/python3

import unittest

# There has to be a better way of doing this
import sys
sys.path.insert(0, '')
from process_sim.temperature_control import TemperatureControl

class TestTemperatureControl(unittest.TestCase):

    def setUp(self):
        self.tc = TemperatureControl(low_bound=40.0, high_bound=50.0)

    def test_init(self):
        print('Testing test_init')
        self.assertEqual(self.tc.low_bound, 40.0)
        self.assertEqual(self.tc.high_bound, 50.0)
        self.assertEqual(self.tc.temperature, 35.0)
        self.assertEqual(self.tc.temp_change, 0.0)
        self.assertEqual(self.tc.running, True)
        self.assertEqual(self.tc.natural_drift, -0.2)
        

if __name__ == '__main__':
    unittest.main()