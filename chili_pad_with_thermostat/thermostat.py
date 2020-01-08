from chili_pad.driver import Driver as CP
import smbus2
import bme280
from aioconsole import ainput
import asyncio

port = 1
address = 0x76
bus = smbus2.SMBus(port)

cp = CP()
cp.pump_on()
cp.off()

def to_farheheit(deg_c):
    return 32 + 9 * deg_c/5

def get_temp():
    data = bme280.sample(bus, address)
    return to_farheheit(data.temperature)

async def get_input():
    global set_temp
    set_temp = 75

    while True:
        i = await ainput(f"")
        print('\n')
        set_temp = float(i)

async def regulate_temp():
    while True:
        temp = get_temp()

        if temp > set_temp + 1:
            pass
            # cp.cool()
        elif temp < set_temp -1:
            pass
            # cp.heat()
        else:
            cp.off()

        print(f'Set: {set_temp:.2f} Actual {temp:.2f} {cp.get_heat_cool()}', end='\n')
        await asyncio.sleep(10)


async def main():
    res = await asyncio.gather(get_input(), regulate_temp())
    return res

# asyncio.run(main())

pass
