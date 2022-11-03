import json
from dataclasses import dataclass

from infrastructure.ddd.serializable import Serializable


@dataclass(frozen=True)
class ScanEnded(Serializable):
    screeningId: str
    finishedDate: str
    redFlags: list

    def toMap(self):
        return self.__dict__

    @classmethod
    def fromMap(cls, myMap: dict):
        return cls(**myMap)
