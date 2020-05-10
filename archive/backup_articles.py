"""This file is for backing up articles from Notes."""
# It should only need to be run once.

import re
import sys
import time
from save_article import SaveArticle
from models.source import Source


class Backup(object):
    def get_data(self):
        with open("./data/backup_articles.txt") as fh:
            return fh.read()

    def split_data(self):
        return DATA.split("***")

    def find_date(self, entry):
        regex = r"(\d\/\d?\d\/20)"
        matches = re.finditer(regex, entry, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            return match.group(0)

    def get_aois(self, entry):
        data = entry.split("Articles of interest:")
        return data[1]

    def get_articles(self, aois):
        articles = re.split("\n\n", aois)
        return articles

    def get_lines(self, article):
        return article.split("\n")


if __name__ == "__main__":
    b = Backup()
    s = Source()
    DATA = b.get_data()
    for entry in b.split_data():

        thedate = b.find_date(entry)
        aois = b.get_aois(entry)
        articles = b.get_articles(aois)

        for article in articles:
            time.sleep(2)
            lines = b.get_lines(article)
            if len(lines) < 3:
                continue

            source_id = s.get_id_from_name(lines[1])
            params = {
                "Title": lines[0],
                "Source": source_id,
                "Date": thedate,
                "URL": lines[2],
            }
            if len(lines) > 3:
                params["URL"] = lines[3]
                params["Notes"] = lines[2]

            else:
                params["Notes"] = ""

            print ""

            sa = SaveArticle(sys.argv[0])
            sa.save(
                url=params["URL"],
                title=params["Title"],
                notes=params["Notes"],
                source_id=params["Source"],
                thedate=params["Date"],
            )
