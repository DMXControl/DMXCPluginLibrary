from typing import List, Optional, Type, TypeVar, Dict

from models.version import Version
from models.dmxcversion import DMXCVersion

T = TypeVar('T')


class Plugin:
    """
    Python class to hold the data parsed from the json file.
    Contains convenience funtions to filter and manipulate plugindata.
    """

    def __init__(self, name: str,author: str, short: str, desc: str, license: str, url: str, iconurl: str, versions: List[Version]) -> None:
        self.name = name
        self.author = author
        self.short = short
        self.desc = desc
        self.license = license
        self.url = url
        self.iconurl = iconurl
        self.versions = versions

    @classmethod
    def fromdict(cls: Type[T], data) -> T:
        versions = []
        if "versions" in data:
            for vers in data["versions"]:
                dmxcvers = [DMXCVersion(ver) for ver in vers["dmxc-version"]]
                versions.append(Version(vers["version"], dmxcvers, vers["url"], vers["hash"]))
        return Plugin(data["name"], data["author"], data["short-desc"], data["desc"], data["license"], data["url"], data["icon-url"], versions)

    def checkversion(self, dmxcversion: DMXCVersion) -> Optional[Version]:
        for version in self.versions:
            if dmxcversion in version.dmxcversion:
                return version
        return None

    def toshortdict(self) -> Dict[str, str]:
        return {"name": self.name, "desc": self.short, "author": self.author, "license": self.license, "icon-url": self.iconurl}

    def __str__(self) -> str:
        return f"{self.name} - [{self.short if len(self.short) < 20 else self.short[0:17] + '...'}]"
