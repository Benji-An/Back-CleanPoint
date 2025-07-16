from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from models import Compra, Usuario, Producto
from schemas import CompraOut
from database import SessionLocal

router = APIRouter(prefix="/compras", tags=["Compras"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calcular_descuento(cleanpoints: int, puntos_por_descuento: int = 10, max_descuento: int = 50) -> int:
    return min(cleanpoints // puntos_por_descuento, max_descuento)

@router.post("/", response_model=CompraOut)
def comprar_producto(
    usuario_id: int = Body(..., embed=True),
    producto_id: int = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not usuario or not producto:
        raise HTTPException(status_code=404, detail="Usuario o producto no encontrado")
    descuento = calcular_descuento(usuario.cleanpoints)
    precio_final = producto.precio * (1 - descuento / 100)
    compra = Compra(
        usuario_id=usuario_id,
        producto_id=producto_id,
        precio_pagado=round(precio_final, 2),
        descuento_aplicado=descuento
    )
    db.add(compra)
    db.commit()
    db.refresh(compra)
    return compra

@router.get("/historial/{usuario_id}", response_model=list[CompraOut])
def historial_compras(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(Compra).filter(Compra.usuario_id == usuario_id).order_by(Compra.fecha.desc()).all()