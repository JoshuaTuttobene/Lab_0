
"""!
@file step_response.py
This file contains code which measures the time response of the output pin voltage in response
to a change from 0-3.3V at the input pin and prints the voltage data along with its
corresponding time in ms.

TODO: Lab 0 Week 2 additions 

@author Aaron Escamilla, Karen Morales De Leon, Joshua Tuttobene
@date   1-16-2024 SPL Original file
@copyright (c) 2024 by Nobody and released under GNU Public License v3
"""

import micropython
import utime
import pyb
import cqueue

# Intialization of pins, and setting them to start at 0
pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP, value=0)
pinB0 = pyb.Pin(pyb.Pin.board.PB0, pyb.Pin.OUT_PP, value=0)
adcB0 = pyb.ADC(pinB0)

micropython.alloc_emergency_exception_buf(100)

Queue_Size = 500
volts = cqueue.IntQueue(Queue_Size)

# Measure and store voltage output from B0
timer_data = pyb.Timer(1, freq=1000)             # Timer for the data at a finer resolutions
timer_input = pyb.Timer(1, freq=200)             # Timer to run the input

# Array for time (works in loop)
time = 0

# Empty array to get collection from ADC readings
# adc_conversion = []

def timer_interrupt(timer_data):
    """!
    timer_interrupt serves to measure the output from pin B0
    Once the queue is full, the callback function stops
    @param   a timer at a 1000Hz to collect data
    @return a queue full of the voltage readings of the first order step response
    """

    output_voltage = volts.put(adcB0.read())     # Reads and puts the data in queue from output (B0)
    if volts.full():                             # Once full, the interrupt no longer runs
        timer_input.callback(None)
        print(volts.any())
    
def step_response():
    """!
    step_response serves to initialize the input from pin C0
    This is done only when the there is space for the queue to be filled
    @param   a timer at a 200Hz to collect data
    @return a queue full of the converted voltage from the readings of the first order step response
    """
    timer_input.callback(timer_interrupt)       # Calls interrupt
    pinC0.high()
    while not volts.full():
        pass
    pinC0.low()

step_response()

for Queue_Size in range(500):
    print(f"{time}, {(3.3/4096)*volts.get()}")
    time = time + 10
if volts.any() == False:
    print("end")
        



    