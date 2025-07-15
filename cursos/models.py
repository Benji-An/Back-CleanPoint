from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Curso(Base):
    __tablename__ = "cursos"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, unique=True, index=True)
    descripcion = Column(String)
    tema = Column(String)
    contenido = Column(String)  # Nuevo campo

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    cleanpoints = Column(Integer, default=0)
    recompensas = relationship("Recompensa", back_populates="usuario")

class Recompensa(Base):
    __tablename__ = "recompensas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    puntos_requeridos = Column(Integer)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="recompensas")
