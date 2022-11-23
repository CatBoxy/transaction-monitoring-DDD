
from fastapi import APIRouter, FastAPI

from infrastructure.persistence.db import DataBase
from infrastructure.persistence.event_store import EventStore

app = FastAPI()

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"],
    responses={404: {"description": "Not found"}},
)



@router.post("/create")
def createAlert():
    try:
        database = DataBase('uif_db')
        eventStore = EventStore(database)
        return [{"username": "Rick"}, {"username": "Morty"}]
    except:
        return 'error'


@router.post("/dismiss")
def dismissAlert():
    try:
        database = DataBase('uif_db')
        eventStore = EventStore(database)
        pass
    except:
        pass


@router.post("/investigate")
def startInvestigation():
    return [{"username": "Rick"}, {"username": "Morty"}]
