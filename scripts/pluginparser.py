import os
from typing import Iterator, List, Tuple

from models.plugin import Plugin
import json


class PluginParser:
    """
    This Class parses all files in a folder and generates plugin objects.
    """

    def __init__(self, path: str) -> None:
        self.files = [os.path.join(path, f) for f in os.listdir(path) if
                      os.path.isfile(os.path.join(path, f)) and "json" in f]

    def getpluginsfile(self) -> Iterator[Tuple[Plugin, str]]:
        for file in self.files:
            with open(file) as f:
                yield Plugin.fromdict(json.load(f)), file

    def getplugins(self) -> Iterator[Plugin]:
        for file in self.files:
            with open(file) as f:
                yield Plugin.fromdict(json.load(f))

    def getpluginslist(self) -> List[Plugin]:
        return list(self.getplugins())
