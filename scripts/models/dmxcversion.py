from enum import Enum


class DMXCVersion(Enum):
    DMXC31 = "3.1"
    DMXC311 = "3.1.1"
    DMXC32 = "3.2"
    DMXC321 = "3.2.1"

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented