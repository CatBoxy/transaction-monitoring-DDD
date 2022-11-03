from fastapi import APIRouter

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)


@router.get("/all")
async def getAllTransactions():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.post("/bulk")
async def addTransactions():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.post("/")
async def addTransaction():
    return [{"username": "Rick"}, {"username": "Morty"}]
