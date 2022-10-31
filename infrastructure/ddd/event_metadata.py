from dataclasses import dataclass
from datetime import datetime

from infrastructure.ddd.message_metadata import MessageMetadata
from infrastructure.valueObjects.date_time import DateTime


@dataclass
class EventMetadata(MessageMetadata):
    __timestamp: float

    def getTimestamp(self) -> float:
        return self.__timestamp

    def getDatetimeUTC(self) -> DateTime:
        date = datetime.utcfromtimestamp(self.__timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return DateTime(date)
