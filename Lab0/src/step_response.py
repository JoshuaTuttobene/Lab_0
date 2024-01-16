
"""!
@file step_response.py
This file contains code which computes the answer to the question of 
Life, the Universe, and Everything. Hopefully it can be done in fewer
than 100,000 years.

TODO: Create a function which explains what the question actually means.
      This might take a bit longer. 

@author Aaron Escamilla, Karen Morales De Leon, Joshua Tuttobene
@date   1-16-2258 SPL Original file
@copyright (c) 2258 by Nobody and released under GNU Public License v3
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
    output_voltage = volts.put(adcB0.read())     # Reads and puts the data in queue from output (B0)
    if volts.full():                             # Once full, the interrupt no longer runs
        timer_input.callback(None)
        print(volts.any())
    """!
    timer_interrupt serves to measure the output from pin B0
    Once the queue is full, the callback function stops
    @param   a timer at a 1000Hz to collect data
    @return a queue full of the voltage readings of the first order step response
    """

def step_response():
    
    timer_input.callback(timer_interrupt)       # Calls interrupt
    pinC0.high()
    while not volts.full():
        pass
    pinC0.low()

step_response()

for Queue_Size in range(500):
    print(f"{time}, {(3.3/4096)*volts.get()}")
    time = time + 10
    
    """!
    step_response serves to initialize the input from pin C0
    This is done only when the there is space for the queue to be filled
    @param   a timer at a 200Hz to collect data
    @return a queue full of the converted voltage from the readings of the first order step response
    """
    



    