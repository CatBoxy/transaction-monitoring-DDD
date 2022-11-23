
from fastapi import APIRouter, FastAPI

from infrastructure.persistence.db import DataBase
from infrastructure.persistence.event_store import EventStore

app = FastAPI()

router = APIRouter(
    prefix="/scanner",
    tags=["scanner"],
    responses={404: {"description": "Not found"}},
)


@router.post("/schedule")
def scheduleScan():
    database = DataBase('uif_db')
    eventStore = EventStore(database)
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.post("/cancel")
def cancelScan():
    database = DataBase('uif_db')
    eventStore = EventStore(database)
    try:
        pass
    except:
        pass

