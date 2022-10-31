from dataclasses import dataclass


@dataclass
class MessageMetadata():
    __messageId: str

    def getMessageId(self) -> str:
        return self.__messageId
