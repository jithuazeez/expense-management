from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import expenses, totals, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Management API",
    description="Track expenses, view totals, and manage your budget.",
    version="1.0.0",
)

app.include_router(users.router)
app.include_router(expenses.router)
app.include_router(totals.router)


@app.get("/")
async def read_root():
    return {"message": "Expense Tracker API — visit /docs for the interactive documentation."}
