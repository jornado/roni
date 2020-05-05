"""
This file is for saving an article to AirTable.

Usage: save_article.py "The Source" http://someurl
"""

from datetime import date
import requests
import sys

from models.article import Article
from models.source import Source
from urler import Urler


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

    def post(self, thing, alt=True):
        headers = {
            "Authorization": "Bearer %s" % thing.config["key"],
            "Content-type": "application/json; charset=utf-8"
        }
        payload = self.format_payload(thing)
        api_url = (thing.alt_api_url if alt else thing.api_url)
        res = requests.post(
            api_url,
            json=payload,
            headers=headers,
        )
        print res.json()


class SaveArticle(Save):
    def __init__(self, prog):
        super(SaveArticle, self).__init__(prog, "url")

    def strip_source(self, text, source):
        return text

    def save(self, url, source_id, thedate):
        u = Urler(url)
        u.fetch()

        title = (u.title if not u.is_apple
                 else self.strip_source(u.title, source_id))

        self.article = Article(
            {
                "URL": url,
                "Title": title,
                "Notes": u.notes,
                "Source": [source_id],
                "MinToRead": u.min_to_read,
                "Date": thedate,
            }
        )
        print "Saving Article"
        print self.article.title
        print self.article.notes
        print url
        print ""

        # TODO: bug with unicode characters posting weirdly to airtable
        # TODO: take Source name out of apple news title
        self.post(self.article)


# Test stuff
if __name__ == "__main__":
    s = SaveArticle(sys.argv[0])
    s.check_args(len(sys.argv) == 3)

    thedate = date.today().isoformat()
    source = Source()
    # uncomment this to update sources
    source.write_sources()
    source_id = source.get_id_from_name(sys.argv[1])
    if not source_id:
        print "No source found for %s" % sys.argv[1]
        exit

    s.save(
        url=sys.argv[2],
        source_id=source_id,
        thedate=thedate,
    )