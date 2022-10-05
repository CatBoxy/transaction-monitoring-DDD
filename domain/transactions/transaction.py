from dataclasses import dataclass
from typing import Optional

from infrastructure.ddd.aggregate import Aggregate
from infrastructure.ddd.aggregate_Id import AggregateId
from infrastructure.valueObjects.account_number import AccountNumber
from infrastructure.valueObjects.amount import Amount
from infrastructure.valueObjects.currency import Currency
from infrastructure.valueObjects.date_time import DateTime
from infrastructure.valueObjects.doc_number import DocNumber
from infrastructure.valueObjects.doc_type import Doctype
from infrastructure.valueObjects.ip import IpAddress
from infrastructure.valueObjects.method import Method
from infrastructure.valueObjects.name import Name
from infrastructure.valueObjects.type import Type
from infrastructure.valueObjects.uuid import UUIDValue


@dataclass(kw_only=True)
class Transaction(Aggregate):
    uuid: UUIDValue
    accountNumber: AccountNumber
    dateTime: DateTime
    type: Type
    method: Method
    amount: Amount
    currency: Currency
    partyDocType: Optional[Doctype]
    partyDocNumber: Optional[DocNumber]
    cleanPartyDocNumber: Optional[DocNumber]
    partyAccountNumber: Optional[AccountNumber]
    partyName: Optional[Name]
    requestIp: Optional[IpAddress]
    externalReference: str

    def getTransactionId(self) -> AggregateId:
        return self.getAggregateId()

    # def createTransaction(self):

