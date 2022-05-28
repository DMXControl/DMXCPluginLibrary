from typing import List
from models.dmxcversion import DMXCVersion


class Version:

    def __init__(self, version: str, dmxcversion: List[DMXCVersion], url: str, hashval: str) -> None:
        self.version = version
        self.dmxcversion = dmxcversion
        self.url = url
        self.hash = hashval
