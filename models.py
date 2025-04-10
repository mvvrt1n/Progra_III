from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Base de datos de SQLAlchemy
Base = declarative_base()

# Tabla de relación muchos a muchos entre personajes y misiones
personaje_mision = Table(
    'personaje_mision',
    Base.metadata,
    Column('personaje_id', Integer, ForeignKey('personajes.id')),  # Relaciona personaje
    Column('mision_id', Integer, ForeignKey('misiones.id'))  # Relaciona misión
)

class Personaje(Base):
    """
    Clase que representa a un personaje en el sistema. Cada personaje tiene un ID, nombre, nivel
    y puntos de experiencia (XP). También tiene una relación con las misiones que puede aceptar
    mediante la tabla de relación 'personaje_mision'.
    """
    __tablename__ = 'personajes'
    id = Column(Integer, primary_key=True)  # Clave primaria: ID del personaje
    nombre = Column(String, nullable=False)  # Nombre del personaje
    nivel = Column(Integer, nullable=False)  # Nivel del personaje
    xp = Column(Integer, default=0)  # Puntos de experiencia (XP) del personaje

    # Relación muchos a muchos con las misiones
    misiones = relationship("Mision", secondary=personaje_mision, back_populates="personajes")


class Mision(Base):
    """
    Clase que representa una misión en el sistema. Cada misión tiene un ID, nombre, descripción
    y nivel requerido para ser aceptada. Además, tiene una relación con los personajes que la
    han aceptado.
    """
    __tablename__ = 'misiones'
    id = Column(Integer, primary_key=True)  # Clave primaria: ID de la misión
    nombre = Column(String, nullable=False)  # Nombre de la misión
    descripcion = Column(String)  # Descripción de la misión
    nivel_requerido = Column(Integer, nullable=False)  # Nivel requerido para aceptar la misión

    # Relación muchos a muchos con los personajes
    personajes = relationship("Personaje", secondary=personaje_mision, back_populates="misiones")
