"""Configuration file stuff."""

import json
from datetime import date


class Config():
    """Methods for configuration."""

    def __init__(self):
        """Init."""
        self.config = Config.get_config()
        self.today = date.today().isoformat()

    @classmethod
    def get_config(cls):
        """Load config options, such as api key and host url."""
        filename = ".config"
        with open(filename) as fh:
            return json.loads(fh.read())
