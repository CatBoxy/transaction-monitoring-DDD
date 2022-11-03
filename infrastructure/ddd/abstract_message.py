from abc import ABC, abstractmethod
from dataclasses import dataclass

from infrastructure.ddd.serializable import Serializable


@dataclass
class AbstractMessage():
    __payload: Serializable

    def getPayload(self) -> Serializable:
        return self.__payload

    def getType(self) -> str:
        return type(self.__payload).__name__
