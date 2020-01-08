from chili_pad.driver import Driver as CP
import matplotlib.pyplot as plt
from simple_pid import PID
from temperature_sense import TemperatureSense

cp = CP()
ts = TemperatureSense()
pid = PID(
    Kp=0.246,
    Ki=0.000839,
    Kd=0,
    setpoint=ts.get_temp_fahrenheit(),
    sample_time=0.5,
    output_limits=(-100,100),

)

setpoint, power, temp, time = [], [], [], []

setpoint = range(100)
time = range(100)
plt.plot(time, setpoint)