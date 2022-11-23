
from dataclasses import dataclass, field
from typing import List, Optional

from infrastructure.ddd.aggregate_Id import AggregateId
from infrastructure.ddd.domain_event import DomainEvent
from infrastructure.ddd.event_stream import EventStream
from infrastructure.ddd.metadata_domain_event import MetadataDomainEvent
from infrastructure.ddd.serializable import Serializable


@dataclass
class Aggregate():
    __aggregateId: AggregateId
    __version: int = field(init=False)
    __events: List[Optional[DomainEvent]] = field(default_factory=lambda: [])

    def __post_init__(self):
        for event in self.__events:
            self.__apply(event)
        self.__version = 0

    def getAggregateId(self) -> AggregateId:
        return self.__aggregateId

    def getVersion(self) -> int:
        return self.__version

    def getPendingEvents(self) -> EventStream:
        eventStream = EventStream(self.__events)
        self.__events = []
        return eventStream

    def _publish(self, event: Serializable):
        self.__version += 1
        metadata = MetadataDomainEvent.newFromAggregate(aggregate=self)
        domainEvent = DomainEvent(event, metadata)
        self.__events.append(domainEvent)
        self.__apply(domainEvent)

    def __apply(self, event: DomainEvent):
        payload = event.getPayload()
        applyName = "_apply" + payload.__class__.__name__
        if hasattr(self, applyName):
            eventApply = getattr(self, applyName)
            eventApply(event)
