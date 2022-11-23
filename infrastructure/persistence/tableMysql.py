from typing import Optional, List

from infrastructure.persistence.db import DataBase


class TableMysql():

    def __init__(self, dataBase, table):
        self.__db = dataBase
        self.__table = table

    def select(
            self,
            projections: Optional[dict] = None,
            conditions: Optional[dict] = None,
            order: Optional[List] = None,
            maxQuant: Optional[int] = None,
            fromLimit: Optional[int] = None
    ) -> str:
        pass

    def where(self, conditions: Optional[dict] = None) -> str:

    def order(self, order: Optional[List] = None) -> str:
        if order is None or len(order) == 0:
            return ''
        return ' ORDER BY ' + ', '.join(order)
    def limit(self) -> str:

    def forUpdate(self) -> str:
