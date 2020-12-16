import datetime
import os
import json

import time


class StatHelper:
    def __init__(self):
        self.counter = 0
    
    def increment(self):
        self.counter += 1

    def print_count(self):
        print(str.format("Total details count: {0}", self.counter))