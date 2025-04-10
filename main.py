from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from models import Personaje, Mision, Base
from cola import Queue

# Creación de la aplicación FastAPI
app = FastAPI()

# Configuración de la base de datos SQLite
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Creación de las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Diccionario para gestionar las colas de misiones por personaje
cola_misiones = {}

# Modelos de Pydantic para validación de datos de entrada
class PersonajeCreate(BaseModel):
    """
    Modelo para la creación de un personaje. Contiene los campos `nombre` y `nivel`.
    """
    nombre: str
    nivel: int

class MisionCreate(BaseModel):
    """
    Modelo para la creación de una misión. Contiene los campos `nombre`, `descripcion` y `nivel_requerido`.
    """
    nombre: str
    descripcion: str
    nivel_requerido: int

@app.post("/personajes/")
def create_personaje(personaje: PersonajeCreate):
    """
    Crea un nuevo personaje en la base de datos y asigna una cola de misiones vacía.
    """
    db = SessionLocal()
    nuevo = Personaje(nombre=personaje.nombre, nivel=personaje.nivel)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    cola_misiones[nuevo.id] = Queue()  # Asignar una cola vacía al personaje
    return nuevo

@app.post("/misiones/")
def create_mision(mision: MisionCreate):
    """
    Crea una nueva misión en la base de datos.
    """
    db = SessionLocal()
    nueva = Mision(
        nombre=mision.nombre,
        descripcion=mision.descripcion,
        nivel_requerido=mision.nivel_requerido
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@app.post("/personajes/{personaje_id}/misiones/{mision_id}")
def aceptar_mision(personaje_id: int, mision_id: int):
    """
    Permite a un personaje aceptar una misión y agregarla a su cola de misiones.
    """
    db = SessionLocal()
    personaje = db.query(Personaje).filter_by(id=personaje_id).first()
    mision = db.query(Mision).filter_by(id=mision_id).first()

    if not personaje or not mision:
        raise HTTPException(status_code=404, detail="Personaje o misión no encontrados")

    personaje.misiones.append(mision)
    db.commit()
    
    if personaje_id not in cola_misiones:
        cola_misiones[personaje_id] = Queue()
    cola_misiones[personaje_id].enqueue(mision.nombre)  # Añadir misión a la cola del personaje

    return {"message": f"Misión '{mision.nombre}' aceptada por {personaje.nombre}"}

@app.post("/personajes/{personaje_id}/completar")
def completar_mision(personaje_id: int):
    """
    Permite a un personaje completar una misión, sumando XP y eliminando la misión de su cola.

    """
    db = SessionLocal()
    personaje = db.query(Personaje).filter_by(id=personaje_id).first()

    if personaje_id not in cola_misiones or cola_misiones[personaje_id].is_empty():
        raise HTTPException(status_code=404, detail="No hay misiones en cola")

    mision_completada = cola_misiones[personaje_id].dequeue()  # Eliminar misión completada de la cola

    # Sumar XP al personaje
    xp_ganado = 10  # Puedes ajustar esto según la misión
    personaje.xp += xp_ganado

    db.commit()

    return {"message": f"Misión completada: {mision_completada}. {personaje.nombre} ha ganado {xp_ganado} XP."}

@app.get("/personajes/{personaje_id}/misiones")
def listar_misiones_en_espera(personaje_id: int):
    """
    Lista todas las misiones en espera de un personaje, es decir, aquellas que están en su cola.
    """
    if personaje_id not in cola_misiones:
        return {"misiones": []}
    return {"misiones": cola_misiones[personaje_id].items}
