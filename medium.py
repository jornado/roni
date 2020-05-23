"""Functions for posting articles to Medium."""
import datetime
import requests

from config import Config
from mailer import Mailer

MEDIUM_POST_URL = "https://api.medium.com/v1/users/%s/posts"


class Medium(object):
    """API for posting to Medium."""

    def __init__(self):
        config = Config.get_config()

        self.author_id = config["medium_author_id"]
        self.username = config["medium_username"]
        self.token = config["medium_access_token"]

    def get_title(self):
        return Mailer.get_subject()

    def get_url(self):
        return "https://medium.com/@%s/rona-report-%s" % (
            self.username, datetime.date.today().isoformat())

    def get_headers(self):
        return {"Authorization": "Bearer %s" % self.token}

    def format(self, html, publish):
        return {
            "title": self.get_title(),
            "url": self.get_url(),
            "contentFormat": "html",
            "content": html,
            "tags": ["covid-19", "coronavirus", "rona"],
            "publishStatus": "public" if publish else "draft",
            "license": "all-rights-reserved",
            "licenseUrl": "https://medium.com/policy/9db0094a1e0f"
        }

    def post(self, html, publish=True):
        return requests.post(
            MEDIUM_POST_URL % self.author_id,
            self.format(html, publish),
            headers=self.get_headers())


if __name__ == "__main__":
    Config.set_debug()
    m = Medium()
    res = m.post("<b>hello</b>", publish=False)
    print res.json()
