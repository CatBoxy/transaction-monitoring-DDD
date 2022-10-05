from fastapi import APIRouter

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)

@router.get("/all")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/bulk")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]