from typing import Union

from fastapi import FastAPI
from application.routers import transactions, alerts, scanner

app = FastAPI()

app.include_router(transactions.router)
app.include_router(alerts.router)
app.include_router(scanner.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
