import utime

pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

while True:
    pinC0.value(0)
    utime.sleep(5)
    pinC0.value(1)
    utime.sleep(5)