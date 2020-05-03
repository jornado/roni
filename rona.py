"""This file contains methods for communicating with AirTable."""

from datetime import date
import json
import requests


class Rona(object):
    """Methods for communicating for Airtable."""

    def __init__(self):
        """Init."""
        self.config = self.get_config()
        self.today = date.today().isoformat()

    def get_config(self):
        """Load config options, such as api key and host url."""
        filename = ".config"
        with open(filename) as fh:
            return json.loads(fh.read())

    def get_sources(self):
        """Load file that contains the id and name of all the news sources."""
        with open("sources.json") as fh:
            data = fh.read()
            return json.loads(data)

    def get_params(self, sort):
        """Parameters sent to the AirTable api when querying a list."""
        params = {
            "api_key": self.config["key"],
        }
        if sort:
            params["sort[0][field]"] = sort,
            params["sort[0][direction]"] = "desc",
            # params["pageSize"] = 10
            # params["filterByFormula"] = "DATE='%s'" % self.today

        return params

    def get_url(self, table):
        """Full URL to an AirTable table."""
        return "{}/{}".format(self.config["host"], table)

    def get_content(self, table, sort="Date"):
        """Pull down a list of items from an AirTable table."""
        url = self.get_url(table)
        params = self.get_params(sort)
        res = requests.get(url, params=params)
        content = res.json()

        if "error" in content:
            print res.url
            print content
            return None

        return content

    def encode(self, text):
        """Encode to UTF-8."""
        if not text:
            return None

        return text
        try:
            return text.encode('utf-8').strip()
        except UnicodeDecodeError:
            return text

    def clean(self, items, klass, date):
        """Clean up the data from the api and put it into objects."""
        cleaned = []
        items = items["records"]
        for item in items:
            if item["fields"]["Date"] != str(date):
                continue
            thing = klass(item["fields"])
            cleaned.append(thing)

        print "Cleaned %d %s items" % (len(cleaned), klass)

        return cleaned
