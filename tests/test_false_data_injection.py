#!/usr/bin/python3

import unittest
import time

# Add root directory to the import path
import sys
sys.path.insert(0, '')
from process_sim.temperature_control import TemperatureControl
from attacks.false_data_injection import FalseDataInjection

class Test_FalseDataInjection(unittest.TestCase):

    def setUp(self):
        self.tc = TemperatureControl(low_bound=40.0, high_bound=50.0)
        self.injection = FalseDataInjection(self.tc)

    def test_init(self):
        print('\tRunning test_init')
        self.assertEqual(self.injection.tc, self.tc)
        self.assertEqual(self.injection.active, False)
        
    def test_attack(self):
        print('\tRunning test_attack')
        start_bound = self.tc.low_bound
        self.assertEqual(start_bound, 40)
        self.tc.start_simulation()
        self.injection.activate()
        self.injection.attack()
        time.sleep(1)
        self.tc.stop_simulation()
        self.assertNotEqual(start_bound, self.tc.low_bound)

    def test_activate(self):
        print('\tRunning test_activate')
        self.assertEqual(self.injection.active, False)
        self.injection.activate()
        self.assertEqual(self.injection.active, True)     

if __name__ == '__main__':
    unittest.main()