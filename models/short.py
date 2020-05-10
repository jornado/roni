from __future__ import absolute_import

from airtable import Airtable


class Short(Airtable):
    """One daily short."""

    def __init__(self, params):
        """Init."""
        super(Short, self).__init__()

        self._content = self.encode(params["Content"])
        self.url = self.encode(params["URL"])
        self.date = (params["Date"] or self.today)

    @property
    def content(self):
        """Text content of short."""
        return self._content
        return self._content.decode('utf-8').strip()

    @property
    def api_url(self):
        """Return API URL."""
        return self.get_url("Shorts")

    def format(self):
        """Format Airtable dict."""
        return {
            "Content": self.content,
            "URL": self.url,
            "Date": self.today,
        }

    def __repr__(self):
        """Text representation of short."""
        repr = ""
        if self.date:
            repr += "\nDate: %s" % self.date
        if self.url:
            repr += "\nURL: %s" % self.url
        if self.content:
            repr += "\nContent: %s" % self.content

        return repr
