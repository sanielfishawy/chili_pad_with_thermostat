from chili_pad.driver import Driver as CP
import time
import datetime as dt
from temperature_sense import TemperatureSense

cp = CP()
ts = TemperatureSense()
f = open('step.txt', 'a+')

def test_loop_times():
    last_time = dt.datetime.now()
    for i in range(100):
        t_loop = dt.datetime.now()
        t_bme = ts.get_temp_data().timestamp
        print(t_loop - last_time)
        print(t_bme - last_time, '\n')

        last_time = t_loop

        time.sleep(.25)

def turn_on_heat():
    cp.pump_on()
    cp.heat()
    cp.set_power(50)

def save_temp_time():
    while(True):
        f.write(f'{ts.to_farheheit(ts.get_temp_data().temperature)}, {time.time()}\n')
        f.flush()
        time.sleep(.25)

turn_on_heat()
save_temp_time()