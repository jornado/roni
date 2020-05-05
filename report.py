"""This file is for outputting the Airtable Report based on airtable rows."""

from chameleon import PageTemplateLoader
from stats import Stats
import datetime
import io
import sys

from airtable import Airtable
from config import Config
from mailer import Mailer
from models.article import Article
from models.short import Short

DATA_DIR = "./data/"
OUT_FILE = "%s/report.html" % DATA_DIR


class Report(object):
    """Format and send the Airtable Report."""

    def __init__(self, thedate=None):
        """Init stuff."""
        self.airtable = Airtable()
        self.date = (thedate.date() or Config.today.date())
        self.config = Config.get_config()
        self.sources = self.airtable.get_sources()

    def stats(self):
        """Get deaths stats for desired states."""
        s = Stats(self.date)
        return s.report()

    def fetch_items(self):
        """Fetch the articles and shorts from Airtable."""
        articles, shorts = self.get_items(self.date)
        self.write_items(articles)

        return (articles, shorts)

    def write_items(self, articles):
        art_urls = [article.url for article in articles]
        self.write("\n".join(art_urls), "%s/articles.txt" % DATA_DIR)

    def format(self, articles, shorts):
        """Templatize the latest articles, shorts, and stats data."""
        print "Parsing items for %s" % self.date

        stats = self.stats()

        templates = PageTemplateLoader("templates")
        template = templates["report.pt"]

        return template(
            articles=articles,
            shorts=shorts,
            stats=stats,
        )

    def write(self, data, filename):
        """Write it out to an HTML file."""
        character_encoding = "utf-8"
        # TODO: bug where data is not unicode
        with io.open(filename, "w", encoding=character_encoding) as fh:
            fh.write(data)

    def get_items(self, date):
        """Templatize the latest articles, shorts, and stats data."""
        print "Parsing items for %s" % date

        articles = self.airtable.clean(
            self.airtable.get_content("Articles", "Date"), Article, self.date)
        shorts = self.airtable.clean(
            self.airtable.get_content("Shorts", "Date"), Short, self.date)

        return (articles, shorts)

    def report(self):
        """Run the full report."""
        articles, shorts = self.fetch_items()
        data = self.format(articles, shorts)
        self.write(data, OUT_FILE)

        return data


if __name__ == "__main__":
    # Uncomment this to update sources
    # from models import Source
    # tmp_source = Source()
    # tmp_source.write_sources()

    # Debug date
    # TODO: mail date bug when date is not today
    # item_date = datetime.datetime.strptime("2020-04-28", "%Y-%m-%d")
    item_date = datetime.datetime.today()

    r = Report(item_date)
    data = r.report()

    if len(sys.argv) > 1:
        print "Uncomment me"
        m = Mailer()
        m.send(data)
    else:
        print "Not sending email in debug mode, see report.html"
