import abc
from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class Serializable(ABC):

    @abc.abstractmethod
    def toMap(self):
        pass

    @classmethod
    @abc.abstractmethod
    def fromMap(cls, myMap: dict):
        pass
