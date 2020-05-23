"""
This file is for parsing the data pulled down from The Atlantic.

Into the format used by the Rona Report.
"""
from __future__ import absolute_import

import collections
import datetime
import functools
import json
import math
import operator

DATA_DIR = "./data"
DATA_FILE = "states.json"
US_FILE = "us.json"
STATES = ["OR", "NY", "NJ", "NC", "DC"]
STAT = "hospitalized_current"


class Stat(object):
    def __init__(self, state, date, thesum, yesterday, change, prevsum):
        self.state = state
        self.date = date
        self.rawsum = thesum
        self.yesterday = yesterday
        self.change = change
        self.prevsum = prevsum
        try:
            self.sum = '{:,}'.format(thesum)
        except ValueError:
            self.sum = 0

    def __repr__(self):
        repr = ""
        if self.state:
            repr += "\nState: %s" % self.state
        if self.date:
            repr += "\nDate: %s" % self.date
        if self.sum:
            repr += "\nSum: %s" % self.sum
        if self.prevsum:
            repr += "\nPrev Sum: %s" % self.prevsum
        if self.change:
            repr += "\nChange: %s\n" % self.change

        return repr


class Stats(object):
    def __init__(self, date=None):
        self.us = json.load(open(DATA_DIR + "/" + US_FILE))
        self.data = json.load(open(DATA_DIR + "/" + DATA_FILE))
        self.states_by_day = {state: self.data[state][STAT]
                              for state in STATES}
        self.stats = []
        self.date = date or datetime.today()
        self.previous_date = self.date - datetime.timedelta(days=7)

    def add_total_to_report(self):
        change = self.get_change(
            self.us[self.date.strftime('%Y-%m-%d')][STAT],
            self.us[self.previous_date.strftime('%Y-%m-%d')][STAT])
        self.stats.append(
            Stat(
                state="US",
                date=self.date,
                thesum=self.us[self.date.strftime('%Y-%m-%d')][STAT],
                yesterday=self.previous_date,
                change=change,
            )
        )

    def report(self):
        for state in STATES:
            this_sum = self.get_7_day_avg(state, self.date)
            prev_sum = self.get_day_stat(state, self.previous_date)
            change = self.get_change(this_sum, prev_sum)

            self.stats.append(
                Stat(
                    state=state,
                    date=self.date,
                    thesum=this_sum,
                    yesterday=self.previous_date,
                    prevsum=prev_sum,
                    change=change,
                )
            )

        self.stats.sort(key=lambda x: x.rawsum, reverse=True)
        # self.add_total_to_report()

        return self.stats

    def get_day_stat(self, state, date):
        for item in self.states_by_day[state]:
            date_str = "%s-%s-%s" % (
                item["year"], item["month"]+1, item["day"])
            item_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")

            if (item_date.strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d")):
                return item["num"]

    def get_item_datestr(self, item):
        date_str = "%s-%s-%s" % (
            item["year"], item["month"]+1, item["day"])
        return datetime.datetime.strptime(date_str, "%Y-%m-%d")

    def get_7_day_avg(self, state, date):
        total = 0
        num_days = 7
        date_list = [date - datetime.timedelta(days=x) for x in range(num_days)]

        for item in self.states_by_day[state]:
            item_date = self.get_item_datestr(item)
            if item_date in date_list:
                date = date - datetime.timedelta(days=1)
                total += item["num"]
        
        return total/num_days

    def get_change(self, this_sum, prev_sum):
        try:
            return int(
                math.ceil((this_sum - prev_sum) / float(prev_sum) * 100))
        except TypeError:
            return 0
        except ZeroDivisionError:
            return 0

    # Sum one stat number across days
    def sum(self, items, stat):
        return dict(functools.reduce(operator.add,
                    map(collections.Counter, items)))[stat]


if __name__ == "__main__":
    # item_date = datetime.datetime.strptime("2020-05-21", "%Y-%m-%d")
    item_date = datetime.datetime.today()
    s = Stats(item_date)
    print s.report()
