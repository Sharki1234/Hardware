from machine import Pin,I2C
import time
import tm1637
from max30102 import MAX30102

display = tm1637.TM1637(clk = Pin(16),dio = Pin(17))
display.brightness(7)
display.write()

i2C = I2C(1, sda=Pin(2),scl=Pin(3),freq=400000)
sensor = MAX30102(i2c = i2C)
sensor.setup_sensor()

last_beat_time = 0
last_ir = 0
bpm_history = []
raw = []

while True:
    sensor.check()
    if sensor.available():
        ir = sensor.pop_ir_from_storage()
        if ir>10000:

            if last_ir>ir:
                current_time = time.ticks_ms()
                if (current_time-last_beat_time)>0:
                    beats = int(60000/(current_time-last_beat_time))
                    last_beat_time = current_time
                    if len(bpm_history)>4:
                        bpm_history.pop(0)
                    bpm_history.append(beats)
                    mean = int(sum(bpm_history)/len(bpm_history))
                    display.number(mean)
                    

            last_ir= ir

        else:
            display.write()



