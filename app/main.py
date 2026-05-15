from fastapi import FastAPI
from app.routers import expenses, totals

app = FastAPI()

app.include_router(expenses.router)
app.include_router(totals.router)

@app.get("/")
async def read_root():
    return{"message": "expense Tracker"}