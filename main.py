#API REST: Es una interfaz de programacion de aplicaciones para compartir recursos
from typing import Optional
import uuid
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

# Inicializamos una variable que tendra todas las caracteristicas de la API REST
app = FastAPI()

#Aca definimos el modelo
class Curso(BaseModel):
    id: str
    nombre: str
    descripcion: Optional[str] = None
    nivel = str
    duracion = int

# Simularemos una base de datos
cursos_db =[]

#CRUD: Read (lectura ) GET ALL: leeremos todos los cursos que hay en la base de datos

@app.get("/cursos/", response_model=list[Curso])

def obtener_cursos():
    return cursos_db

# CRUD: Create (escribir) POST: creamos un nuevo curso en la base de datos

@app.post("/cursos/", response_model=Curso) #Aca apunta solo a un curso, porque es lo que vamos a agregar   

def crear_curso(curso:Curso):
    curso.id=str(uuid.uuid4())
    #uuid es un generador de ID unicos. En este caso lo pasamos por str porque estamos esperando ese tipo de dato
    cursos_db.append(curso)

#CRUD: Read (lectura) GET (individual): Leeremos el curso con el ID que pidamos

@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id: str):
    #next es un metodo que nos ayuda a buscar un solo curso, en este caso, dentro de una lista
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) #Con nexto tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

#CRUD: Update(actualizar/modificar) PUT: Modificaremos un recurso con el ID que pidamos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None):
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso) #Con esto buscamos el indice exacto donde esta el curso en nuestra lista
    cursos_db[index] = curso_actualizado
    return curso_actualizado

#CRUD: Delete (eliminar) DELETE: Eliminaremos un recurso con el ID que pidamos

@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id: str):

    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) #Con nexto tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso



