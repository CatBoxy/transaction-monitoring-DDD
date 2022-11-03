import uuid
from copy import copy
from dataclasses import dataclass
from time import time

from infrastructure.ddd.aggregate import Aggregate
from infrastructure.ddd.event_metadata import EventMetadata


@dataclass
class MetadataDomainEvent(EventMetadata):
    __sequence: int
    __aggregate: str
    __aggregateId: str
    __orderNumber: int

    def getSequence(self) -> int:
        return self.__sequence

    def getAggregate(self) -> str:
        return self.__aggregate

    def getAggregateId(self) -> str:
        return self.__aggregateId

    def getOrderNumber(self) -> int:
        return self.__orderNumber

    def withSequence(self, sequence: int):
        if self.__sequence > 0:
            raise ValueError('Secuencia ya asignada')
        metadata = copy(self)
        metadata.__sequence = sequence
        return metadata

    @staticmethod
    def newFromAggregate(aggregate: Aggregate):
        metadataDomainEvent = MetadataDomainEvent(
            __messageId=str(uuid.uuid4()),
            __timestamp=time(),
            __sequence=-1,
            __aggregate=type(aggregate).__name__,
            __aggregateId=aggregate.getAggregateId().getUUID().myUuid,
            __orderNumber=aggregate.getVersion()
        )
        return metadataDomainEvent
