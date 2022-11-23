import codecs
import csv
import time

from fastapi import APIRouter, FastAPI, File, UploadFile

from application.commands.add_bulk_transactions_command import AddBulkCommand
from application.services.add_bulk_transactions_service import AddBulkService
from infrastructure.persistence.db import DataBase
from infrastructure.persistence.event_store import EventStore
from infrastructure.persistence.transaction_aggregate_repository import TransactionRepository
from infrastructure.persistence.transaction_indexes_repository import TransactionIndexRepository

app = FastAPI()

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)


@router.get("/all")
def getAllTransactions():
    database = DataBase('uif_db')
    time.sleep(5)
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.post("/bulk")
async def addTransactions(file: UploadFile = File(...)):
    try:
        database = DataBase('uif_db')
        eventStore = EventStore(database)
        transactionRepo = TransactionRepository(eventStore)
        transactionIndexRepo = TransactionIndexRepository(database)
        uploadedFile = file.file
        if not uploadedFile:
            return "No se cargo el archivo"

        csvInput = csv.DictReader(codecs.iterdecode(uploadedFile, 'utf-8'))
        command = AddBulkCommand(csvInput)
        service = AddBulkService(transactionRepo, transactionIndexRepo, database)
        service.run(command)
        return "archivo {filename} cargado satisfactoriamente".format(filename=file.filename)

    except:
        return 'error'


@router.post("/")
def addTransaction():
    return [{"username": "Rick"}, {"username": "Morty"}]


    # def lazy(csvfile):
    #     with open(csvfile) as f:
    #         r = csv.reader(f)
    #         for row in r:
    #             yield row
    # columnHeaders = next(lazy(file.filename))
    #
    # for piece in lazy(file.filename):
    #     txDict = dict(zip(columnHeaders, piece))
    #     if list(txDict.keys())[0] != list(txDict.values())[0]:
    #         command = AddBulkCommand(txDict)
    #         service = AddBulkService(transactionRepo)
    #         service.run(command)
    # with open(file.filename, 'r') as myFile:
    #     for line in myFile:
    #         print(line)
