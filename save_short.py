"""
This file is for saving a short to AirTable.

It's not really used, because it's actually not that much of a time saver.
"""

import sys
import datetime
from models import Short
import requests


class Save(object):
    def __init__(self, prog, args):
        self.prog = prog
        self.args = args

    def usage(self):
        return "%s [%s]" % (self.prog, self.args)

    def check_args(self, is_valid):
        if not is_valid:
            print "Invalid args!"
            print self.usage()
            sys.exit()

    def format_payload(self, thing):
        payload = {}
        payload["records"] = [{"fields": thing.format()}]
        payload["typecast"] = True
        return payload

    def post(self, thing):
        headers = {
            "Authorization": "Bearer %s" % thing.config["key"],
        }
        payload = self.format_payload(thing)
        print payload
        res = requests.post(
            thing.api_url,
            json=payload,
            headers=headers,
        )
        print res.json()


class SaveShort(Save):
    def __init__(self, prog):
        super(SaveShort, self).__init__(prog, "url")

    def save(self, content, date, url=None):
        self.short = Short(
            {
                "URL": url,
                "Content": content,
                "Date": date,
            }
        )
        print self.short
        self.post(self.short)


# Test stuff
if __name__ == "__main__":
    s = SaveShort(sys.argv[0])
    s.check_args(len(sys.argv) == 3)

    # uncomment this to update sources
    # tmp_source = Source()
    # tmp_source.write_sources()

    s.save(
        content=sys.argv[1],
        url=sys.argv[2],
        date=datetime.date.today().isoformat(),
    )
