from pydantic import BaseModel

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

class RecompensaOut(RecompensaBase):
    id: int
    usuario_id: int
    class Config:
        orm_mode = True
