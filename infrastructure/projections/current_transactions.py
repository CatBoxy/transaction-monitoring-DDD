from dataclasses import dataclass

from infrastructure.ddd.projection import Projection
from infrastructure.persistence.db import DataBase


@dataclass
class CurrentTransactions(Projection):
    __db: DataBase

    def create(self):
        pass

    def empty(self):
        pass

    def addTransaction(
            self,
            transactionId: str,
            accountNumber: str,
            dateTime: str,
            loadedDateTime: str,
            type: str,
            method: str,
            amount: str,
            currency: str,
            partyDocType: str,
            partyDocNumber: str,
            partyAccountNumber: str,
            partyName: str,
            requestIp: str,
            externalReference: str
    ):
        def callback():
            values = (
                transactionId,
                accountNumber,
                dateTime,
                loadedDateTime,
                type,
                method,
                amount,
                currency,
                partyDocType,
                partyDocNumber,
                partyAccountNumber,
                partyName,
                requestIp,
                externalReference
            )
            sql = "INSERT INTO current_transactions (" \
                  "transactionId, " \
                  "accountNumber, " \
                  "dateTime, " \
                  "loadedDateTime, " \
                  "type, " \
                  "method, " \
                  "amount, " \
                  "currency, " \
                  "partyDocType, " \
                  "partyDocNumber, " \
                  "partyAccountNumber, " \
                  "partyName, " \
                  "requestIp, " \
                  "externalReference) VALUES (" \
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.__db.execute(sql, values)

        self.__db.executeInTransaction(callback)
