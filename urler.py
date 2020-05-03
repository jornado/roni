import requests
from bs4 import BeautifulSoup
import readtime


class Urler(object):
    def __init__(self, url):
        self.title = ""
        self.notes = ""
        self.url = url
        self.min_to_read = 0

    def get(self):
        res = requests.get(self.url)
        self.soup = BeautifulSoup(res.text, "lxml")
        return self.soup

    def get_meta(self):
        self.title = self.soup.find("meta",  property="og:title")["content"]
        self.notes = self.soup.find(
            "meta",  property="og:description")["content"]

    def get_readtime(self):
        for script in self.soup(["script", "style"]):
            script.decompose()
        text = self.soup.get_text()

        r = readtime.of_text(text)
        self.min_to_read = r.minutes

    def __repr__(self):
        """Return text representation."""
        repr = ""
        if self.title:
            repr += "Title: %s" % self.title.encode('utf-8')
        if self.min_to_read:
            repr += "\nMin to read: %d" % self.min_to_read
        if self.url:
            repr += "\nURL: %s" % self.url
        if self.notes:
            repr += "\nNotes: %s" % self.notes.encode('utf-8')

        return repr


if __name__ == "__main__":
    url = "https://apple.news/A3Cb8bxFtSGmCDvCQmqi2pg"
    url = "https://www.nytimes.com/interactive/2020/04/30/opinion/coronavirus-covid-vaccine.html"
    url = "https://www.wweek.com/news/2020/04/29/oregon-has-hundreds-of-excess-deaths-suggesting-a-hidden-covid-19-toll/"
    url = "https://blogs.scientificamerican.com/observations/masks-and-emasculation-why-some-men-refuse-to-take-safety-precautions/"
    url = "https://www.theatlantic.com/ideas/archive/2020/05/trumps-macabre-declarations-victory/611029/"
    url = "https://www.fastcompany.com/90498707/how-nike-built-face-shields-from-shoe-parts-in-just-two-weeks"

    u = Urler(url)
    u.get()
    u.get_meta()
    u.get_readtime()
    print u
