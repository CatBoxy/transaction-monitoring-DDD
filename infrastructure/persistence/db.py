import mysql.connector
from mysql.connector import Error


class DataBase():
    def __init__(self, db):
        try:
            self.connection = mysql.connector.connect(
                port="3306",
                host="127.0.0.1",
                user="root",
                password="2154625",
                db=db
            )
            self.cursor = self.connection.cursor()
            print('coneccion establecida')
        except Error as ex:
            print('Error al conectar: {0}'.format(ex))

    def initTransaction(self):
        try:
            print("Iniciando transaccion")
            self.connection.start_transaction()
        except Error as ex:
            print('Error al iniciar transaccion: {0}'.format(ex))

    def commit(self):
        if self.inTransaction():
            raise Exception('Ninguna transaccion en curso')
        try:
            print("ejecutando commit")
            self.connection.commit()
        except Error as ex:
            print('Error al ejecutar commit: {0}'.format(ex))

    def rollback(self):
        if self.inTransaction():
            raise Exception('Ninguna transaccion en curso')
        try:
            print('Ejecutando rollback')
            self.connection.rollback()
        except Error as ex:
            print('Error al ejecutar rollback: {0}'.format(ex))

    def inTransaction(self):
        return self.connection.in_transaction

    def executeInTransaction(self, callback):
        self.initTransaction()
        try:
            callback()
            self.commit()
        except Error as ex:
            if self.inTransaction():
                self.rollback()
            print('Error al ejecutar transaccion: {0}'.format(ex))

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
        except Error as ex:
            print('Error al ejecutar sentencia sql: {0}'.format(ex))
