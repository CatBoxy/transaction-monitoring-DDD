from copy import copy
from dataclasses import dataclass
from infrastructure.ddd.abstract_message import AbstractMessage
from infrastructure.ddd.metadata_domain_event import MetadataDomainEvent


@dataclass
class DomainEvent(AbstractMessage):

    __metadata: MetadataDomainEvent

    def getMetadata(self) -> MetadataDomainEvent:
        return self.__metadata

    def setMetadata(self, newMetadata: MetadataDomainEvent):
        self.__metadata = newMetadata

    def withSequence(self, sequence: int):
        event = copy(self)
        event.__metadata = self.__metadata.withSequence(sequence)
        return event

    # def getOrderNumber ???
