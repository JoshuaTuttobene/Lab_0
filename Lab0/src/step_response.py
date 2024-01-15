import micropython
import utime
pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)
micropython.alloc_emergency_exception_buf(100)
timmy = pyb.Timer (1, freq = 200)             # Timer 1 running at 100 Hz
timmy.counter ()                              # Get timer value

# Define a function that toggles the pin and set it as the interrupt
# service routine. Uses pinC0 from above

def toggler (which_timer):
    
    if pinC0.value():
        pinC0.value(0)
        start_time = utime.ticks_us()
    else:
        pinC0.value(1)
        end_time = utime.ticks_us()    
        duration = utime.ticks_diff(end_time, start_time)
        print(duration)
    

def step_response():
    #make a list for time and voltage, CSV
    #start a clock when the input is initialized
    #measure voltage, record time simultaneously
    #repeat every 10ms until voltage ~= 3.3V
    #print end
    
    timmy.callback(toggler)
    
    
while True:   
    step_response()
    
    
    

    


