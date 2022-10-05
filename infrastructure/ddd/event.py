from dataclasses import dataclass

from infrastructure.ddd.abstract_message import AbstractMessage


@dataclass
class Event(AbstractMessage):

    __metadata: EventMetadata

    def getMetadata(self) -> EventMetadata:
        return self.