from fastapi import FastAPI
from routers import cursos, usuarios, recompensas, marketplace, compras
from models import Base
from database import engine

app = FastAPI(title="Backend de CleanPoints", version="1.0.0")

app.include_router(cursos.router)
app.include_router(usuarios.router)
app.include_router(recompensas.router)
app.include_router(marketplace.router)
app.include_router(compras.router)

Base.metadata.create_all(bind=engine)
