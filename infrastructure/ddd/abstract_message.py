from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AbstractMessage(ABC):

    __payload: dict

    def getPayload(self) -> dict:
        return self.__payload

