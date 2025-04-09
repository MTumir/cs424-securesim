# ICS Security Final Project: SecureSim

## Contributors
* Max Tumir
* Munib Ahmed
* Brandon Nanhthanong
* Jackson Price

## Description

In order to simulate a model for a temperature control system 
of a chemical tank, a basic version was made in Python using a 
natural decay in temperature and a system that heats the target 
if it falls below a lower bound. The simulation is currently split 
into three main parts:
* temperature_control.py - Holds the basic variables and functions 
related to the chemical tank
* tc_controller.py - Holds functions for starting and stopping the
simulation
* main.py - The driver file which starts and stops the simulation
while printing information to the console

## Setting up the program

    Prerequisites:

-Python 3.6 or higher
-pip (python package manager)

1. Clone the repository:
-git clone [repository-url]
cd cs424-securesim

2. Install the required dependencies

pip install -r requirements.txt

## Running the program

1. Navigate to the project directory:
    
    cd cs424-securesim

2. Run the main program:
    
    python main.py

    This program will start a temperature simulation that runs for 2000 seconds. You can monitor the temperature and change the rate in real-time. 
