"""This file is for backing up shorts from Notes."""
# It should only need to be run once.

import re
import sys
import time
from save_short import SaveShort
from models.source import Source


class Backup(object):
    def get_data(self):
        with open("./data/backup_shorts.txt") as fh:
            return fh.read()

    def split_data(self):
        return DATA.split("***")

    def find_date(self, entry):
        regex = r"(\d\/\d?\d\/20)"
        matches = re.finditer(regex, entry, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            return match.group(0)

    def get_aois(self, entry):
        data = entry.split("In short:")
        return data[1]

    def get_shorts(self, aois):
        shorts = re.split("\*", aois, re.MULTILINE)
        return shorts

    def get_lines(self, short):
        return short.split("\n")

    def get_content(self, content):
        m = re.match('(.+)(https?://.+)', content)
        if not m:
            return content, None
        return m.group(1), m.group(2)


if __name__ == "__main__":
    b = Backup()
    s = Source()
    DATA = b.get_data()
    for entry in b.split_data():

        thedate = b.find_date(entry)
        aois = b.get_aois(entry)
        shorts = b.get_shorts(aois)

        for short in shorts:
            time.sleep(2)
            lines = b.get_lines(short)
            content, url = b.get_content(lines[0].strip())

            params = {
                "Content": content,
                "Date": thedate,
                "URL": url,
            }

            sa = SaveShort(sys.argv[0])
            sa.save(
                content=params["Content"],
                date=params["Date"],
                url=params["URL"],
            )
