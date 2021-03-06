import time
import datetime

class TempProgram:
    '''
    Set up simple profile.
        - Start temp.
        - Hold time for start temp.
        - Downward temp ramp.
        - Rate of temp drop for down ramp.
        - Minimum temp
    '''

    def __init__(
            self,
            start_temp=97,
            start_temp_hold_time=60 * 60, # seconds
            temp_drop_rate=.001, # deg F per second
            min_temp=75,
    ):
        self.start_temp = start_temp
        self.start_temp_hold_time = start_temp_hold_time
        self.temp_drop_rate = temp_drop_rate
        self.min_temp = min_temp
        self.start_time = None
        self.start_date = None


    def start(self):
        self.start_time = time.monotonic()
        self.start_date = datetime.datetime.now()

    def time_since_start(self):
        if self.is_running():
            return time.monotonic() - self.start_time
        else:
            return 0

    def get_temp(self):
        time_in_ramp = self.time_since_start() - self.start_temp_hold_time
        if time_in_ramp < 0:
            return self.start_temp
        else:
            return self.get_ramp_temp(time_in_ramp)

    def get_ramp_temp(self, time_in_ramp):
        result = self.start_temp - (time_in_ramp * self.temp_drop_rate)
        return max(result, self.min_temp)

    def is_in_start_hold(self):
        return self.time_since_start() < self.start_temp_hold_time

    def is_running(self):
        return self.start_time is not None

    def reset(self):
        self.start_time = None
        self.start_date = None
        return "Reset"

    def set_min_temp(self, min_temp: float):
        self.min_temp = min_temp
        return self.min_temp

    def get_min_temp(self):
        return self.min_temp

    def set_start_temp(self, start_temp):
        self.start_temp = float(start_temp)
        return self.start_temp

    def get_start_temp(self):
        return self.start_temp

    def set_start_temp_hold_time(self, hold_time:int):
        self.start_temp_hold_time = hold_time
        return self.start_temp_hold_time

    def get_start_temp_hold_time(self):
        return self.start_temp_hold_time

    def set_temp_drop_rate(self, rate:float):
        self.temp_drop_rate = rate
        return self.temp_drop_rate

    def get_temp_drop_rate(self):
        return self.temp_drop_rate