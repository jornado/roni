import json

from airtable import Airtable


class Source(Airtable):
    """Article source newspaper."""

    def __init__(self, id=None):
        """Init."""
        super(Source, self).__init__()
        if id:
            self.id = self.encode(id)

    @property
    def name(self):
        """Name."""
        return self.encode(self.get_sources()[self.id])

    def get_id_from_name(self, name):
        """Reverse dict and get ID."""
        by_name = dict(map(reversed, self.get_sources().items()))
        return by_name[name]

    def write_sources(self):
        """Write sources to a JSON file."""
        with open("data/sources.json", "w") as fh:
            fh.write(json.dumps(
                self.get_sources_from_api(), indent=2))

    def get_sources_from_api(self):
        """Return all sources from Airtable API."""
        all_sources = {}
        sources = self.get_content("Sources", False)
        for source in sources["records"]:
            all_sources[source["id"]] = source["fields"]["Name"]

        return all_sources

    def __repr__(self):
        """Text representation of source."""
        repr = ""
        if self.id:
            repr += "\n\tID: %s" % self.id
        if self.name:
            repr += "\n\tName: %s" % self.name

        return repr
