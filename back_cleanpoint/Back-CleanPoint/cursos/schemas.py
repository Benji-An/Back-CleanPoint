from pydantic import BaseModel
from datetime import datetime

class CursoBase(BaseModel):
    titulo: str
    descripcion: str
    tema: str
    contenido: str  # Nuevo campo

class CursoCreate(CursoBase):
    pass

class CursoOut(CursoBase):
    id: int

    class Config:
        orm_mode = True

class UsuarioBase(BaseModel):
    nombre: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioOut(UsuarioBase):
    id: int
    cleanpoints: int
    class Config:
        orm_mode = True

class RecompensaBase(BaseModel):
    nombre: str
    puntos_requeridos: int

class RecompensaCreate(RecompensaBase):
    pass

class RecompensaOut(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None
    puntos_requeridos: int
    usuario_id: int | None = None  # Solo si existe este campo en el modelo

    class Config:
        orm_mode = True

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    precio: float

class ProductoCreate(ProductoBase):
    pass

class ProductoOut(ProductoBase):
    id: int
    class Config:
        orm_mode = True

class CompraBase(BaseModel):
    usuario_id: int
    producto_id: int
    precio_pagado: float
    descuento_aplicado: int

class CompraCreate(CompraBase):
    pass

class CompraOut(CompraBase):
    id: int
    fecha: datetime

    class Config:
        orm_mode = True
