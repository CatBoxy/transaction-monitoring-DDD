from dataclasses import dataclass

from infrastructure.ddd.abstract_message import AbstractMessage
from infrastructure.ddd.event_metadata import EventMetadata


@dataclass(frozen=True)
class Event(AbstractMessage):
    __metadata: EventMetadata

    def getMetadata(self) -> EventMetadata:
        return self.__metadata
