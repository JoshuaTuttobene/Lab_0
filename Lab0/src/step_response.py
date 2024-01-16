import micropython
import utime
import pyb
#machine.reset()

pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)
micropython.alloc_emergency_exception_buf(100)
timmy = pyb.Timer(1, freq=200)             # Timer 1 running at 200 Hz for a 10ms function period
timmy.counter()                            # Get timer value

up_time = 0
down_time = 0
duration = 0
time = 0

# Define a function that toggles the pin and set it as the interrupt
# service routine. Uses pinC0 from above
def toggler(which_timer):
    if pinC0.value():
        pinC0.value(0)
        global up_time
        up_time = utime.ticks_us()
    else:
        pinC0.value(1)
        global down_time
        down_time = utime.ticks_us()

def step_response():

    timmy.callback(toggler)
    global duration
    duration = abs(utime.ticks_diff(down_time, up_time) * 2 / 1000)
    global time
    time += duration
    print(time)

while True:
    step_response()
