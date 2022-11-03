import json
from dataclasses import dataclass

from infrastructure.ddd.serializable import Serializable


@dataclass(frozen=True)
class AlertAttached(Serializable):
    investigationId: str
    attachedDate: str
    alertId: str

    def toMap(self):
        return self.__dict__

    @classmethod
    def fromMap(cls, myMap: dict):
        return cls(**myMap)
