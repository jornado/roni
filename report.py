"""This file is for outputting the Rona Report based on airtable rows."""

from chameleon import PageTemplateLoader
from mailer import Mailer
from rona import Rona
from stats import Stats
import datetime
import io
import sys
from models import Article, Short

OUT_FILE = "report.html"


class Report(object):
    """Format and send the Rona Report."""

    def __init__(self, date=None):
        """Init stuff."""
        self.rona = Rona()
        self.date = (date.date() or self.rona.today.date())
        self.config = self.rona.get_config()
        self.sources = self.rona.get_sources()

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
        self.write("\n".join(art_urls), "articles.txt")

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
        with io.open(filename, "w", encoding=character_encoding) as fh:
            fh.write(data)

    def get_items(self, date):
        """Templatize the latest articles, shorts, and stats data."""
        print "Parsing items for %s" % date

        articles = self.rona.clean(
            self.rona.get_content("Articles", "Date"), Article, self.date)
        shorts = self.rona.clean(
            self.rona.get_content("Shorts", "Date"), Short, self.date)

        return (articles, shorts)

    def report(self):
        """Run the full report."""
        articles, shorts = self.fetch_items()
        data = self.format(articles, shorts)
        self.write(data, OUT_FILE)


if __name__ == "__main__":
    # Uncomment this to update sources
    # from models import Source
    # tmp_source = Source()
    # tmp_source.write_sources()

    # Debug date
    # item_date = datetime.datetime.strptime("2020-04-28", "%Y-%m-%d")
    item_date = datetime.datetime.today()

    r = Report(item_date)
    r.report()

    if len(sys.argv) > 1:
        print "Uncomment me"
        # m = Mailer()
        # m.send(data)
    else:
        print "Not sending email in debug mode, see report.html"
