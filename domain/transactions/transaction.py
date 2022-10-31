from dataclasses import dataclass

import uuid

from domain.events.transaction_created import TransactionCreated
from infrastructure.ddd.aggregate import Aggregate
from infrastructure.ddd.aggregate_Id import AggregateId

from infrastructure.valueObjects.payment_type import PaymentType


@dataclass
class Transaction(Aggregate):

    def getTransactionId(self) -> AggregateId:
        return self.getAggregateId()

    @classmethod
    def create(
            cls,
            uuid,
            accountNumber,
            dateTime,
            loadedDateTime,
            type,
            method,
            amount,
            currency,
            partyDocType,
            partyDocNumber,
            cleanPartyDocNumber,
            partyAccountNumber,
            partyName,
            requestIp,
            externalReference
    ):
        transaction = Transaction(__aggregateId=uuid)
        transactionCreated = TransactionCreated(
            transactionId=uuid,
            accountNumber=accountNumber,
            dateTime=dateTime,
            loadedDateTime=loadedDateTime,
            type=type,
            method=method,
            amount=amount,
            currency=currency,
            partyDocType=partyDocType,
            partyDocNumber=partyDocNumber,
            cleanPartyDocNumber=cleanPartyDocNumber,
            partyAccountNumber=partyAccountNumber,
            partyName=partyName,
            requestIp=requestIp,
            externalReference=externalReference
        )
        transaction._publish(transactionCreated)
        return transaction

    def _applyTransactionCreated(self, event: TransactionCreated):
        self.loaded = True
        self.loadedDate = event.loadedDateTime

    def getLoadedTime(self):
        return self.loadedDate


myUuid = str(uuid.uuid4())
transaction = Transaction.create(
    uuid=myUuid,
    accountNumber='654',
    dateTime="2022-09-16 20:15:20",
    loadedDateTime="2022-10-25 10:15:20",
    type='incoming_payment',
    method='debit_card',
    amount='45',
    currency='ARS',
    partyDocType='DNI',
    partyDocNumber='38.091.922',
    cleanPartyDocNumber='38091922',
    partyAccountNumber='415',
    partyName='Juan',
    requestIp='192.0.2.1',
    externalReference='external reference'
)

print(transaction)
print(transaction.getTransactionId())
print(transaction.loadedDate)
print(transaction.loaded)
print(transaction.getVersion())
