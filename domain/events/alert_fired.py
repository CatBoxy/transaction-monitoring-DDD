import json
from dataclasses import dataclass
from typing import Tuple, Union

from infrastructure.ddd.serializable import Serializable


@dataclass(frozen=True)
class RuleParam():
    name: str
    value: str

    def toMap(self):
        return self.__dict__

    @classmethod
    def fromMap(cls, myMap: dict):
        return cls(**myMap)


@dataclass(frozen=True)
class AlertFired(Serializable):
    alertId: str
    accountId: str
    screeningId: str
    creationDateTime: str
    redFlag: str
    dateFrom: str
    dateTo: str
    params: Tuple[RuleParam, ...]
    transactions: list

    def toMap(self):
        return self.__dict__

    @classmethod
    def fromMap(cls, myMap: dict):
        myParams = myMap['params']
        myMap['params'] = []
        for param in myParams:
            myMap['params'].append(RuleParam.fromMap(param))
        myMap['params'] = tuple(myMap['params'])
        return cls(**myMap)
