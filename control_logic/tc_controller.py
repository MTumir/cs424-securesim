#!/usr/bin/python3

'''
Filename: tc_controller.py
Created: 4/7/2025
Updated: 4/7/2025
Description: Provides a controller for TemperatureControl.
'''

class TC_Controller:
    def __init__(self, tc):
        self.tc = tc

    def control_loop(self):
        temperature = self.tc.get_temperature