import datetime
import os
import json

import time


class FileHelper:
    
    def watch_start(self):
        self.start = time.time()

    def watch_stop(self):
        self.stop = time.time()

    def print_diff(self):
        value = self.stop - self.start

        valueD = (((value/365)/24)/60)
        Days = int(valueD)

        valueH = (valueD-Days)*365
        Hours = int(valueH)

        valueM = (valueH - Hours)*24
        Minutes = int(valueM)

        valueS = (valueM - Minutes)*60
        Seconds = int(valueS)

        print(str.format("Days: {0}; Hours {1}; Minutes {2}; Seconds {3}", Days, Hours, Minutes, Seconds))
