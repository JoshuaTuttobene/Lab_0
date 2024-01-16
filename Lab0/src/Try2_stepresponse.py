import micropython
import utime
import pyb
import cqueue

pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP, value=0)
pinB0 = pyb.Pin(pyb.Pin.board.PB0, pyb.Pin.OUT_PP)
adcB0 = pyb.ADC (pinB0)

micropython.alloc_emergency_exception_buf(100)

Queue_Size = 200
volts = cqueue.IntQueue(Queue_Size)

# Q: How to call interrupt in function
# # Input loop
# while not volts.full():
#     if pinC0.high():
#        pinC0.low()   # when wave goes high
#     
#     else:
#        pinC0.high()   # when wave goes low

# Measure and store voltage output from B0
timer_data = pyb.Timer(1, freq=1000)
timer_input = pyb.Timer(1, freq=200)             # Timer 1 running at 200 Hz for a 10ms function period

def timer_interrupt(timer_data):
    output_voltage = volts.put(adcB0.read())
    if volts.full():
        timer_input.callback(None)

def step_response():
    
    timer_input.callback(timer_interrupt)
    pinC0.high()
    while not volts.full():
        pass
    pinC0.low()
    print(volts)
    
    
step_response()


    