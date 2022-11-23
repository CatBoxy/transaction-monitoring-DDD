import uuid
from dataclasses import dataclass
from datetime import datetime
import pytz

from domain.transactions.transaction import Transaction
from infrastructure.persistence.db import DataBase
from infrastructure.persistence.transaction_aggregate_repository import TransactionRepository
from infrastructure.persistence.transaction_indexes_repository import TransactionIndexRepository
from infrastructure.valueObjects.account_number import AccountNumber
from infrastructure.valueObjects.date_time import DateTime
from infrastructure.valueObjects.doc_number import DocNumber
from infrastructure.valueObjects.ip import IpAddress
from infrastructure.valueObjects.money import Money
from infrastructure.valueObjects.name import Name
from infrastructure.valueObjects.payment import Payment
from infrastructure.valueObjects.uuid import UUIDValue


@dataclass
class AddBulkService():
    __repo: TransactionRepository
    __indexRepo: TransactionIndexRepository
    __db: DataBase

    def run(self, command):
        for row in command.fileData:
            transaction = Transaction.create(
                uuid=UUIDValue(str(uuid.uuid4())),
                accountNumber=AccountNumber(row['accountNumber']),
                dateTime=DateTime(row['dateTime']),
                loadedDateTime=DateTime(datetime.now(tz=pytz.UTC).strftime("%Y-%m-%d %H:%M:%S")),
                type=Payment(row['type'], row['method']),
                method=Payment(row['type'], row['method']),
                amount=Money(row['amount'], row['currency']),
                currency=Money(row['amount'], row['currency']),
                partyDocType=DocNumber(row['partyDocNumber'], row['partyDocType']),
                partyDocNumber=DocNumber(row['partyDocNumber'], row['partyDocType']),
                partyAccountNumber=AccountNumber(row['partyAccountNumber']),
                partyName=Name(row['partyName']),
                requestIp=IpAddress(row['requestIp']),
                externalReference=row['externalReference']
            )
            self.__db.initTransaction()
            try:
                isCreated = self.__indexRepo.isCreated(row['externalReference'])
                if not isCreated:
                    self.__indexRepo.saveIndex(row['externalReference'])
                    self.__repo.save(transaction)
                self.__db.commit()
            except:
                self.__db.rollback()
