"""
This file is for copying over articles from Possible Articles to Articles
"""
from __future__ import absolute_import

import requests

from airtable import Airtable
from models.article import Article


class Copy(object):
    def __init__(self):
        self.airtable = Airtable()

    def format_payload(self, thing):
        payload = {}
        payload["records"] = [{"fields": thing.format()}]
        payload["typecast"] = True
        return payload

    def get_possible_articles(self):
        params = {"filterByFormula": "AND(Use = 1)"}
        possible, _ = self.airtable.get_content(
            "Possible Articles", "Date", 0, params)

        return possible

    def headers(self, thing):
        return {
            "Authorization": "Bearer %s" % thing.config["key"],
            "Content-type": "application/json; charset=utf-8"
        }

    def delete_possible_article(self, article):
        res = requests.delete(
            self.possibles[0].alt_api_url + "/" + article.id,
            headers=self.headers(article)
        )
        print res.json()

    def copy_possible_article(self, thing):
        payload = self.format_payload(thing)
        res = requests.post(
            thing.api_url,
            json=payload,
            headers=self.headers(thing),
        )
        print res.json()


class CopyPossibleArticle(Copy):
    def __init__(self):
        super(CopyPossibleArticle, self).__init__()
        self.possibles = []

    def go(self):
        self.get_possibles()

        print "Copying"
        for p in self.possibles:
            self.copy_possible_article(p)

        print "Deleting"
        for p in self.possibles:
            self.delete_possible_article(p)

    def get_possibles(self):
        possible = self.get_possible_articles()
        for p in possible["records"]:
            params = p["fields"]
            params["id"] = p["id"]
            self.possibles.append(Article(params))


if __name__ == "__main__":
    s = CopyPossibleArticle()
    s.go()
