import time
from chili_pad.driver import Driver as CP
import matplotlib.pyplot as plt
from pid import PID
from temperature_sense import TemperatureSense

cp = CP()
cp.pump_on()

ts = TemperatureSense()
pid = PID(
    Kp=20,
    Ki=0.02,
    Kd=0,
    setpoint=75,
    sample_time=0.5,
    output_limits=(-100,100),

)

setpoint, power, temp, time_s = [], [], [], []

while True:
    temp = ts.get_temp_fahrenheit()
    power = pid(temp)
    cp.set_abs_power(power)
    print(f'Temp: {temp:0.2f}  {cp.get_heat_cool()} Power:{cp.get_power()} Components: {pid.components}')
    time.sleep(2)