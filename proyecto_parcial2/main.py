from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from proyecto_parcial2.db.database import create_db_and_tables
from proyecto_parcial2.routers import auth, users

app = FastAPI(title="Proyecto Parcial 2 - Autenticación")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(auth.router)
app.include_router(users.router)