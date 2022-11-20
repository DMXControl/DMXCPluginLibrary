from enum import Enum


class DMXCVersion(Enum):

    DMXC32 = "3.2"
    DMXC321 = "3.2.1"
    DMXC322 = "3.2.2"
    DMXC323 = "3.2.3"

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented