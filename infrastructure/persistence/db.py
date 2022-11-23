import uuid
from collections import deque
from typing import List, Tuple, Optional

import mysql.connector
from mysql.connector import Error

from infrastructure.ddd.aggregate_Id import AggregateId
from infrastructure.ddd.event_stream import EventStream


class DataBase():
    def __init__(self, db):
        try:
            self.__connection = mysql.connector.connect(
                port="3306",
                host="127.0.0.1",
                user="root",
                password="2154625",
                db=db
            )
            self.cursor = self.__connection.cursor()
            self.__savepoints = []
            print('coneccion establecida')
        except Error as ex:
            print('Error al conectar: {0}'.format(ex))

    def initTransaction(self):
        try:
            if self.inTransaction() == 1:
                while True:
                    savepoint = 'SP' + str(uuid.uuid4()).replace('-', '')
                    if savepoint not in self.__savepoints:
                        break
                sql = "SAVEPOINT " + savepoint
                cursor = self.__connection.cursor()
                print('Iniciando Savepoint ' + savepoint)
                cursor.execute(sql)
                self.__savepoints.append(savepoint)
            else:
                self.__savepoints = []
                print("Iniciando transaccion")
                self.__connection.start_transaction()
        except Error as ex:
            print('Error al iniciar transaccion: {0}'.format(ex))

    def commit(self):
        try:
            if self.inTransaction() == 0:
                raise Exception('Ninguna transaccion en curso')
            if len(self.__savepoints) == 0:
                print("ejecutando commit")
                self.__connection.commit()
            else:
                savepoint = self.__savepoints[-1]
                sql = "RELEASE SAVEPOINT " + savepoint
                cursor = self.__connection.cursor()
                cursor.execute(sql)
                self.__savepoints.pop()
        except Error as ex:
            print('Error al ejecutar commit: {0}'.format(ex))

    def rollback(self):
        try:
            if self.inTransaction() == 0:
                raise Exception('Ninguna transaccion en curso')
            if len(self.__savepoints) == 0:
                print('Ejecutando rollback')
                self.__connection.rollback()
            else:
                savepoint = self.__savepoints[-1]
                sql = "ROLLBACK TO SAVEPOINT " + savepoint
                cursor = self.__connection.cursor()
                cursor.execute(sql)
                self.__savepoints.pop()

        except Error as ex:
            print('Error al ejecutar rollback: {0}'.format(ex))

    def inTransaction(self) -> int:
        return self.__connection.in_transaction

    def executeInTransaction(
            self,
            callback,
            aggregateId: Optional[AggregateId] = None,
            eventStream: Optional[EventStream] = None
    ):
        self.initTransaction()
        try:
            if aggregateId is None and eventStream is None:
                callback()
                self.commit()
            if aggregateId is None and eventStream is not None:
                callback(eventStream)
                self.commit()
            else:
                callback(aggregateId, eventStream)
                self.commit()
        except Error as ex:
            if self.inTransaction() == 1:
                self.rollback()
            print('Error al ejecutar transaccion: {0}'.format(ex))
            raise ex

    def result(self, sql: str, values: Optional[Tuple]) -> List:
        try:
            cursor = self.__connection.cursor()
            if values is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, values)
            columnNames = cursor.column_names
            allRows = cursor.fetchall()
            rowsFound = []
            rowsDeque = deque(rowsFound)

            # Genera un deque de dicts con cada row devuelto
            for row in allRows:
                if len(columnNames) == len(row):
                    rowsDeque.appendleft({columnNames[i]: row[i] for i, _ in enumerate(row)})
            return list(rowsDeque)
        except Error as ex:
            print('Error al buscar: {0}'.format(ex))

    def execute(self, sql: str, values: Tuple):
        try:
            cursor = self.__connection.cursor()
            cursor.execute(sql, values)
        except Error as ex:
            print('Error al ejecutar sentencia sql: {0}'.format(ex))



