import micropython
import utime
import pyb
import cqueue

pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP, value=0)
pinB0 = pyb.Pin(pyb.Pin.board.PB0, pyb.Pin.OUT_PP, value=0)
adcB0 = pyb.ADC(pinB0)

micropython.alloc_emergency_exception_buf(100)

Queue_Size = 500
volts = cqueue.IntQueue(Queue_Size)

# Measure and store voltage output from B0
timer_data = pyb.Timer(1, freq=1000)
timer_input = pyb.Timer(1, freq=200)             # Timer 1 running at 200 Hz for a 10ms function period
time = list(range(0, 1991, 10))
adc_conversion = []

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
    
    i = 0
    while i < volts.available():
        adc_conversion.append(3.3*volts.get()/4096)
        i = i+1
        
    #print(volts) # convert later to volts
    
    #print(f"{time}, {adc_conversion}")
    print(f"{time}")
    print(f"{adc_conversion}")
    
step_response()


    