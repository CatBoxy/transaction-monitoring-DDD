from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AbstractMessage():
    __payload: Payload

    def getPayload(self) -> Payload:
        return self.__payload

    def getType(self) -> str:
        return type(self.__payload).__name__
