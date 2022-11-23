from dataclasses import dataclass

from domain.events.transaction_created import TransactionCreated
from infrastructure.ddd.aggregate import Aggregate
from infrastructure.ddd.aggregate_Id import AggregateId
from infrastructure.ddd.domain_event import DomainEvent
from infrastructure.valueObjects.account_number import AccountNumber
from infrastructure.valueObjects.date_time import DateTime
from infrastructure.valueObjects.doc_number import DocNumber
from infrastructure.valueObjects.ip import IpAddress
from infrastructure.valueObjects.money import Money
from infrastructure.valueObjects.name import Name
from infrastructure.valueObjects.payment import Payment
from infrastructure.valueObjects.uuid import UUIDValue


@dataclass
class Transaction(Aggregate):

    def getTransactionId(self) -> str:
        return self.getAggregateId().getUUID()

    @classmethod
    def create(
            cls,
            uuid: UUIDValue,
            accountNumber: AccountNumber,
            dateTime: DateTime,
            loadedDateTime: DateTime,
            type: Payment,
            method: Payment,
            amount: Money,
            currency: Money,
            partyDocType: DocNumber,
            partyDocNumber: DocNumber,
            partyAccountNumber: AccountNumber,
            partyName: Name,
            requestIp: IpAddress,
            externalReference: str
    ):
        transaction = Transaction(AggregateId(uuid.myUuid))
        transactionCreated = TransactionCreated(
            transactionId=uuid.myUuid,
            accountNumber=accountNumber.number,
            dateTime=dateTime.dateTime,
            loadedDateTime=loadedDateTime.dateTime,
            type=type.transactionType,
            method=method.transactionMethod,
            amount=amount.number,
            currency=currency.currency,
            partyDocType=partyDocType.docType,
            partyDocNumber=partyDocNumber.number,
            partyAccountNumber=partyAccountNumber.number,
            partyName=partyName.name,
            requestIp=requestIp.address,
            externalReference=externalReference
        )
        transaction._publish(transactionCreated)
        return transaction

    def _applyTransactionCreated(self, event: DomainEvent):
        self.loaded = True
        eventType = event.getPayload().__class__.__name__
        if eventType == self.__class__.__name__:
            self.loadedDate = event.getPayload().loadedDateTime

    def getLoadedTime(self):
        return self.loadedDate
