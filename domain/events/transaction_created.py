import json
from dataclasses import dataclass
from typing import Optional

from infrastructure.ddd.serializable import Serializable


@dataclass(frozen=True)
class TransactionCreated(Serializable):
    transactionId: str
    accountNumber: str
    dateTime: str
    loadedDateTime: str
    type: str
    method: str
    amount: str
    currency: str
    externalReference: str
    partyDocType: Optional[str] = None
    partyDocNumber: Optional[str] = None
    partyAccountNumber: Optional[str] = None
    partyName: Optional[str] = None
    requestIp: Optional[str] = None

    def toMap(self):
        return self.__dict__

    @classmethod
    def fromMap(cls, myMap: dict):
        return cls(**myMap)
