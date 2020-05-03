"""
This file is for parsing the data pulled down from The Atlantic.

Into the format used by the Rona Report.
"""

import datetime
import collections
import functools
import json
import math
import operator

DATA_DIR = "../src/data/"
DATA_FILE = "states.json"
STATES = ["OR", "NY", "NJ", "NC", "DC"]
STAT = "deaths"


class Stat(object):
    def __init__(self, state, date, thesum, yesterday, change):
        self.state = state
        self.date = date
        self.rawsum = thesum
        self.yesterday = yesterday
        self.change = change
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
        if self.change:
            repr += "\nChange: %s\n" % self.change

        return repr


class Stats(object):
    def __init__(self, date=None):
        self.data = json.load(open(DATA_DIR + DATA_FILE))
        self.states_by_day = {state: self.data[state][STAT]
                              for state in STATES}
        self.stats = []
        self.date = date or datetime.today()
        self.previous_date = self.date - datetime.timedelta(days=1)

    def report(self):
        for state in STATES:
            this_sum = self.get_day_stat(state, self.date)
            prev_sum = self.get_day_stat(state, self.previous_date)
            change = self.get_change(this_sum, prev_sum)

            self.stats.append(
                Stat(
                    state=state,
                    date=self.date,
                    thesum=this_sum,
                    yesterday=self.previous_date,
                    change=change,
                )
            )

        self.stats.sort(key=lambda x: x.rawsum, reverse=True)

        return self.stats

    def get_day_stat(self, state, date):
        for item in self.states_by_day[state]:
            date_str = "%s-%s-%s" % (
                item["year"], item["month"]+1, item["day"])
            item_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")

            if (item_date.strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d")):
                return item["num"]

    def get_change(self, this_sum, prev_sum):
        try:
            return int(
                math.ceil((this_sum - prev_sum) / float(prev_sum) * 100))
        except TypeError:
            return 0

    # Sum one stat number across days
    def sum(self, items, stat):
        return dict(functools.reduce(operator.add,
                    map(collections.Counter, items)))[stat]


if __name__ == "__main__":
    # item_date = datetime.datetime.strptime("2020-04-26", "%Y-%m-%d")
    item_date = datetime.datetime.today()
    s = Stats(item_date)
    print s.report()
