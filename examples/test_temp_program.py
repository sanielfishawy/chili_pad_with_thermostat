#pylint: disable=wrong-import-position, invalid-name
import time
import sys

sys.path.append('../chili_pad_with_thermostat')
from chili_pad_with_thermostat.temp_program import TempProgram

temp_program = TempProgram('/home/pi/chili_pad_with_thermostat/data/temp_profile_test.yml')


s = time.monotonic()
for second in range(0, 5):
    print(round(time.monotonic() - s), temp_program.get_temp(), temp_program.get_mode())
    time.sleep(1)

temp_program.start()
while True:
    print(round(time.monotonic() - s), temp_program.get_temp(), temp_program.get_mode())
    time.sleep(1)

