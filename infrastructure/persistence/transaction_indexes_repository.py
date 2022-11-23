from dataclasses import dataclass

from infrastructure.persistence.db import DataBase


@dataclass
class TransactionIndexRepository():
    __db: DataBase

    def saveIndex(self, externalReference: str):
        def callback():
            value = (externalReference,)
            sql = "INSERT INTO transaction_indexes (transaction_index) VALUES (%s)"
            self.__db.execute(sql, value)
        self.__db.executeInTransaction(callback)

    def isCreated(self, externalReference: str) -> bool:
        value = (externalReference,)
        sql = "SELECT count(*) as quantity FROM transaction_indexes WHERE transaction_index = %s FOR UPDATE"
        regs = self.__db.result(sql, value)
        return regs[0]['quantity'] != 0
