from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models import Base, Curso, Usuario, Recompensa
from database import engine, SessionLocal
from schemas import CursoCreate, CursoOut, UsuarioCreate, UsuarioOut, RecompensaCreate, RecompensaOut

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Cursos Ambientales")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/cursos/", response_model=CursoOut)
def crear_curso(curso: CursoCreate, db: Session = Depends(get_db)):
    # Validar duplicados por titulo
    if db.query(Curso).filter(Curso.titulo == curso.titulo).first():
        raise HTTPException(status_code=400, detail="Ya existe un curso con ese título")
    db_curso = Curso(**curso.dict())
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

@app.get("/cursos/", response_model=list[CursoOut])
def listar_cursos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    return db.query(Curso).offset(skip).limit(limit).all()

@app.get("/cursos/{curso_id}", response_model=CursoOut)
def obtener_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

@app.put("/cursos/{curso_id}", response_model=CursoOut)
def actualizar_curso(curso_id: int, curso: CursoCreate, db: Session = Depends(get_db)):
    db_curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not db_curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    for key, value in curso.dict().items():
        setattr(db_curso, key, value)
    db.commit()
    db.refresh(db_curso)
    return db_curso

@app.delete("/cursos/{curso_id}", response_model=dict)
def eliminar_curso(curso_id: int, db: Session = Depends(get_db)):
    db_curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not db_curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    db.delete(db_curso)
    db.commit()
    return {"detail": "Curso eliminado exitosamente"}

@app.post("/usuarios/", response_model=UsuarioOut)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = Usuario(nombre=usuario.nombre)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.get("/usuarios/{usuario_id}/cleanpoints", response_model=int)
def consultar_cleanpoints(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario.cleanpoints

@app.post("/usuarios/{usuario_id}/reclamar_recompensa/", response_model=RecompensaOut)
def reclamar_recompensa(usuario_id: int, recompensa: RecompensaCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.cleanpoints < recompensa.puntos_requeridos:
        raise HTTPException(status_code=400, detail="No tienes suficientes cleanpoints")
    usuario.cleanpoints -= recompensa.puntos_requeridos
    db_recompensa = Recompensa(**recompensa.dict(), usuario_id=usuario_id)
    db.add(db_recompensa)
    db.commit()
    db.refresh(db_recompensa)
    db.commit()
    return db_recompensa

@app.post("/usuarios/{usuario_id}/completar_curso/{curso_id}", response_model=UsuarioOut)
def completar_curso(usuario_id: int, curso_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not usuario or not curso:
        raise HTTPException(status_code=404, detail="Usuario o curso no encontrado")
    # Ejemplo: sumar 10 cleanpoints por curso completado
    usuario.cleanpoints += 10
    db.commit()
    db.refresh(usuario)
    return usuario

@app.get("/recompensas/", response_model=list[RecompensaOut])
def listar_recompensas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Recompensa).offset(skip).limit(limit).all()

@app.post("/recompensas/", response_model=RecompensaOut)
def crear_recompensa(recompensa: RecompensaCreate, db: Session = Depends(get_db)):
    db_recompensa = Recompensa(**recompensa.dict())
    db.add(db_recompensa)
    db.commit()
    db.refresh(db_recompensa)
    return db_recompensa
