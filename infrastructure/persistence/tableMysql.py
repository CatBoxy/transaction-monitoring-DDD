from typing import Optional, List

from infrastructure.persistence.db import DataBase


class TableMysql():

    def __init__(self, dataBase, table):
        self.__db: DataBase = dataBase
        self.__table = table

    def select(
            self,
            projections: Optional[List] = None,
            conditions: Optional[List] = None,
            order: Optional[List] = None,
            maxQuant: Optional[int] = None,
            fromLimit: Optional[int] = None
    ) -> str:
        pass

    def replace(self, fields: dict):
        placeholders = ()
        values = tuple(dict.values(fields))
        columnFields = tuple(dict.keys(fields))

        for name in fields:
            placeholders = (*placeholders, "%s")

        columnNames = ', '.join(columnFields)
        placeholdersString = ', '.join(placeholders)

        sql = "REPLACE INTO {tableName} ({columnNames}) VALUES ({placeholdersString})".format(
            tableName=self.__table,
            columnNames=columnNames,
            placeholdersString=placeholdersString,
        )
        return self.__db.result(sql, values)

    # def count(self, conditions) -> int:
    #     sql = "SELECT COUNT(*) FROM {tableName}".format(tableName=self.__table)

    def where(self, conditions: Optional[dict] = None) -> str:
        pass

    def order(self, order: Optional[List] = None) -> str:
        if order is None or len(order) == 0:
            return ''
        return ' ORDER BY ' + ', '.join(order)

    def limit(self, maxQuant: int, fromLimit: int = 0) -> str:
        if maxQuant > 0:
            if fromLimit <= 0:
                fromLimit = 0
            return " LIMIT {fromLimit}, {maxQuant}".format(fromLimit=fromLimit, maxQuant=maxQuant)
        else:
            return ''
    def forUpdate(self) -> str:
        if self.__db.inTransaction():
            return ' FOR UPDATE'
        else:
            return ''
