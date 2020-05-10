from __future__ import absolute_import

import re

from airtable import Airtable
from models.source import Source


class Article(Airtable):
    """One Article from Airtable."""

    def __init__(self, params):
        """Init."""
        super(Article, self).__init__()
        self._title = None
        self._notes = None
        self.url = None
        self.data = self.today
        self.source_id = None
        self.source = None
        self.min_to_read = None

        if "Title" in params:
            self._title = self.encode(self.parse_title(params["Title"]))
            self._title = params["Title"]
        if "Notes" in params:
            self._notes = self.encode(params["Notes"])
        if "URL" in params:
            self.url = self.encode(params["URL"])
        if "Date" in params:
            self.date = self.encode(params["Date"])
        if "Source" in params:
            self.source_id = params["Source"][0]
            self.source = Source(params["Source"][0])
        if "MinToRead" in params:
            self.min_to_read = params["MinToRead"]

    @property
    def is_apple(self):
        return re.search("apple.news", self.url)

    @property
    def title(self):
        """Title."""
        if not self._title:
            return ""
        if self.is_apple:
            try:
                return self._title.encode('iso-8859-1').strip()
            except UnicodeEncodeError:
                return self._title
        else:
            return self._title

    @property
    def notes(self):
        """Notes."""
        if not self._notes:
            return ""
        if self.is_apple:
            try:
                return self._notes.encode('iso-8859-1').strip()
            except UnicodeEncodeError:
                return self._title
        else:
            return self._notes

    @property
    def api_url(self):
        """Return API URL."""
        return self.get_url("Articles")

    @property
    def alt_api_url(self):
        """Return Possible Articles API URL."""
        return self.get_url("Possible%20Articles")

    def parse_title(self, title):
        """Parse title out of string that might contain minutes."""
        regex = r".+\((\d\d?) min\)"
        m = re.match(regex, title)
        if m:
            self.min_to_read = m.group(1)
            title = re.sub(r"\(\d+ min\)", "", title)

        return title

    def format(self):
        """Format in Airtable dict."""
        formatted = {
            "Title": self.title,
            "URL": self.url,
            "Date": self.date,
            "Source": [self.source.id],
        }
        if self.min_to_read:
            formatted["MinToRead"] = self.min_to_read
        if self.notes:
            formatted["Notes"] = self.notes

        return formatted

    def __repr__(self):
        """Return text representation."""
        repr = ""
        if self.title:
            repr += "Title: %s" % self.title
        if self.min_to_read:
            repr += "\nMin to Read: %s" % self.min_to_read
        if self.date:
            repr += "\nDate: %s" % self.date
        if self.source:
            repr += "\nSource: %s" % self.source
        if self.url:
            repr += "\nURL: %s" % self.url
        if self.notes:
            repr += "\nNotes: %s" % self.notes
        if self.min_to_read:
            repr += "\nMin to Read: %s" % self.min_to_read

        return repr
