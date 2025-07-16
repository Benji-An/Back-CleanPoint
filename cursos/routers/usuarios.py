from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Usuario, Curso
from schemas import UsuarioCreate, UsuarioOut
from database import SessionLocal

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UsuarioOut)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = Usuario(nombre=usuario.nombre)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.get("/{usuario_id}/cleanpoints", response_model=int)
def consultar_cleanpoints(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario.cleanpoints

@router.post("/{usuario_id}/completar_curso/{curso_id}", response_model=UsuarioOut)
def completar_curso(usuario_id: int, curso_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not usuario or not curso:
        raise HTTPException(status_code=404, detail="Usuario o curso no encontrado")
    usuario.cleanpoints += 10
    db.commit()
    db.refresh(usuario)
    return usuario