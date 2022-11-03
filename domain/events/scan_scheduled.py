import json
from dataclasses import dataclass

from infrastructure.ddd.serializable import Serializable


@dataclass(frozen=True)
class ScanScheduled(Serializable):
    screeningId: str
    startingDate: str
    redFlags: list
    periodStart: str
    periodEnd: str
    isFullScan: bool

    def toMap(self):
        return self.__dict__

    @classmethod
    def fromMap(cls, myMap: dict):
        return cls(**myMap)
