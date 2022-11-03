import json
from dataclasses import dataclass

from infrastructure.ddd.serializable import Serializable


@dataclass(frozen=True)
class InvestigationClosed(Serializable):
    investigationId: str
    closingDate: str

    def toMap(self):
        return self.__dict__

    @classmethod
    def fromMap(cls, myMap: dict):
        return cls(**myMap)
