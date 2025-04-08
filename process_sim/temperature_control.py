#!/usr/bin/python3

'''
Filename: temp_control.py
Created: 4/7/2025
Updated: 4/7/2025
Description: Simulates a temperature control system.
'''

class TemperatureControl:
    def __init__(self, low_bound, high_bound):
        self.low_bound = low_bound      # Lowest temperature before adjustment
        self.high_bound = high_bound    # Highest temperature before adjustment
        self.temperature = 50.0         # Current temperature
        self.temp_change = 0.0          # Current tick's change in temperature

    def update(self):
        self.temperature += self.temp_change

    def set_temp_change(self, change):
        self.temp_change = change

    def get_temperature(self):
        return self.temperature