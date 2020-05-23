"""Configuration file stuff."""
from __future__ import absolute_import

import httplib
import json
import logging
from datetime import date


class Config():
    """Methods for configuration."""

    def __init__(self):
        """Init."""
        self.config = Config.get_config()
        self.today = Config.today()

    @classmethod
    def today(cls):
        return date.today().isoformat()

    @classmethod
    def get_config(cls):
        """Load config options, such as api key and host url."""
        filename = "./data/.config"
        with open(filename) as fh:
            return json.loads(fh.read())

    @classmethod
    def set_debug(self):
        httplib.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        req_log = logging.getLogger('requests.packages.urllib3')
        req_log.setLevel(logging.DEBUG)
        req_log.propagate = True
