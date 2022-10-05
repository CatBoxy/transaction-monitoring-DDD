from abc import ABC
from dataclasses import dataclass, field
from typing import List

from infrastructure.ddd.aggregate_Id import AggregateId


@dataclass(kw_only=True)
class Aggregate(ABC):
    __aggregateId: AggregateId
    __version: int = field(init=False)
    # __eventFlow: EventFlow = field(init=False)
    # __pendingEvents: List[Event]

    # def __post_init__(self):
    #     if self.__eventFlow is not None:
    #         for event in self.__eventFlow:
    #             self.__version += 1
    #             self.apply(event)

    def getAggregateId(self) -> AggregateId:
        return self.__aggregateId

    def getVersion(self) -> int:
        return self.__version

    def _publish(self, event: Event):
        self.__version += 1
        metadata = DomainEventmetadata.newFromAggregate(self)
        domainEvent = DomainEvent(metadata=metadata, event=event)
        self.__pendingEvents.append(domainEvent)
        self.apply(domainEvent)

    # def apply(self):
