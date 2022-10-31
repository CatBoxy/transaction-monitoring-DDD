from dataclasses import dataclass
from typing import List

from infrastructure.ddd.domain_event import DomainEvent


@dataclass
class EventStream():
    __events: List[DomainEvent]

    def getEvents(self) -> List:
        return self.__events

    def getAmount(self) -> int:
        return len(self.__events)

    def isEmpty(self) -> bool:
        if len(self.__events) == 0:
            return False
        else:
            return True

