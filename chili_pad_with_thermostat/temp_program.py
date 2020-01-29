#pylint: disable=line-too-long

import time
import datetime
import yaml

class TempProgram:
    '''
    Set up a versitile profile from data in a yml file describing the profile.
    '''
    START_TEMP = 'start_temp'
    END_TEMP = 'end_temp'
    DURATION = 'duration'
    DURATION_SECONDS = 'duration_seconds'
    TIME_UNIT = 'time_unit'
    HOUR = 'hour'
    MINUTE = 'minute'
    SECOND = 'second'
    SEGMENT_START = 'segment_start'
    SEGMENT_END = 'segment_end'

    MODE = 'mode'
    MODE_HEAT_ONLY = 'heat_only'
    MODE_COOL_ONLY = 'cool_only'
    MODE_HEAT_AND_COOL = 'heat_and_cool'
    MODES = [MODE_HEAT_ONLY, MODE_COOL_ONLY, MODE_HEAT_AND_COOL]

    def __init__(
            self,
            profile_yml,
    ):
        self.profile_yml = profile_yml
        self.profile = None
        self.load_profile(self.profile_yml)

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

    def is_running(self):
        return self.start_time is not None

    def reset(self):
        self.start_time = None
        self.start_date = None
        self.load_profile(self.profile_yml)
        return "Reset"

    def load_profile(self, profile_yml):
        with open(profile_yml, 'r') as yml:
            obj = yaml.load(yml)
        self.profile = self.normalize_profile(obj)
        return obj

    def get_current_segment(self):
        i = 0
        for segment in self.profile:
            if self.time_since_start() <= segment[self.__class__.SEGMENT_END]:
                break
            i += 1
        return self.profile[min(i, len(self.profile) - 1)]

    def get_current_segment_start_temp(self):
        return self.get_current_segment()[self.__class__.START_TEMP]

    def get_current_segment_end_temp(self):
        return self.get_current_segment()[self.__class__.END_TEMP]

    def get_initial_temp(self):
        return self.profile[0][self.__class__.START_TEMP]

    def get_time_in_segment(self):
        return self.time_since_start() - self.get_current_segment()[self.__class__.SEGMENT_START]

    def get_temp(self):
        if self.time_is_past_last_segment():
            return self.get_last_segment()[self.__class__.END_TEMP]

        start_temp = self.get_current_segment_start_temp()
        end_temp = self.get_current_segment_end_temp()
        fraction_of_segment = self.get_time_in_segment() / self.get_current_segment()[self.__class__.DURATION_SECONDS]
        return start_temp + ((end_temp - start_temp) * fraction_of_segment)

    def time_is_past_last_segment(self):
        return self.time_since_start() > self.get_last_segment()[self.__class__.SEGMENT_END]

    def get_last_segment(self):
        return self.profile[-1]

    def normalize_profile(self, profile):
        for segment in profile:
            segment[self.__class__.DURATION_SECONDS] = self.get_duration_seconds(segment)

        last_segment_end = -1
        for segment in profile:
            segment[self.__class__.SEGMENT_START] = last_segment_end + 1
            segment[self.__class__.SEGMENT_END] = segment[self.__class__.SEGMENT_START] + segment[self.__class__.DURATION_SECONDS] - 1
            last_segment_end = segment[self.__class__.SEGMENT_END]
        return profile

    def get_duration_seconds(self, segment):
        if segment[self.__class__.TIME_UNIT] == self.__class__.HOUR:
            return segment[self.__class__.DURATION] * 3600
        elif segment[self.__class__.TIME_UNIT] == self.__class__.MINUTE:
            return segment[self.__class__.DURATION] * 60
        elif segment[self.__class__.TIME_UNIT] == self.__class__.SECOND:
            return segment[self.__class__.DURATION]
        else:
            err = f"Unknown {self.__class__.TIME_UNIT} should be: "
            err += f"'{self.__class__.HOUR}', "
            err += f"'{self.__class__.MINUTE}' or "
            err += f"'{self.__class__.SECOND}'"
            raise KeyError(err)

    def get_mode(self):
        seg = self.get_current_segment()
        if self.__class__.MODE in seg:
            mode = seg[self.__class__.MODE]
            self.raise_if_bad_mode(mode)
        else:
            mode = self.__class__.MODE_HEAT_AND_COOL
        return mode

    def raise_if_bad_mode(self, mode):
        if mode not in self.__class__.MODES:
            raise KeyError(f'Unknown mode. Should be: {self.__class__.MODES}')




