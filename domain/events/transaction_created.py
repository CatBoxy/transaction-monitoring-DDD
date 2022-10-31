from dataclasses import dataclass
from typing import Optional


from infrastructure.valueObjects.account_number import AccountNumber
from infrastructure.valueObjects.amount import Amount
from infrastructure.valueObjects.currency import Currency
from infrastructure.valueObjects.date_time import DateTime
from infrastructure.valueObjects.doc_number import DocNumber
from infrastructure.valueObjects.doc_type import Doctype
from infrastructure.valueObjects.ip import IpAddress
from infrastructure.valueObjects.method import Method
from infrastructure.valueObjects.name import Name
from infrastructure.valueObjects.payment_type import PaymentType
from infrastructure.valueObjects.uuid import UUIDValue


@dataclass(frozen=True)
class TransactionCreated():
    transactionId: UUIDValue
    accountNumber: AccountNumber
    dateTime: DateTime
    loadedDateTime: DateTime
    type: PaymentType
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
