pinA5 = pyb.Pin(pyb.Pin.board.PA5, pyb.Pin.OUT_PP)
tim2 = pyb.Timer(2, freq=0.1)
ch2 = tim2.channel(2, pyb.Timer.PWM, pin=pinA5)
ch2.pulse_width_percent(50)