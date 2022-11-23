from __future__ import annotations
import uuid
from copy import copy
from dataclasses import dataclass
from time import time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
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
    def newFromAggregate(aggregate: Aggregate) -> 'MetadataDomainEvent':
        metadataDomainEvent = MetadataDomainEvent(
            str(uuid.uuid4()),
            time(),
            -1,
            type(aggregate).__name__,
            aggregate.getAggregateId().getUUID(),
            aggregate.getVersion()
        )
        return metadataDomainEvent
