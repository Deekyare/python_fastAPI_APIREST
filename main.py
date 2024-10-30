# Iniciaremos una variable donde tendrá todas las características de una API REST
from typing import Optional
from uuid import uuid4
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

# Acá definimos el modelo
class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int
    
# Simularemos una base de datos
cursos_db = []

# CRUD: Read (lectura)  GET ALL: Leeremos todos los cursos que  haya en la db

@app.get('/cursos/', response_model=list[Curso])
def obtener_cursos():
    return cursos_db

# CRUD: Create (escribir) Post: agregamos un nuevo recurso a nuestra base de datos
@app.post('/cursos/', response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4())
    cursos_db.append(curso)
    return curso
    
# CRUD: Read (lectura) GET (individual): Leeremos el curso que coincida con el ID que pidamos
@app.get('/cursos/{curso_id}', response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next ((curso for curso in cursos_db if curso.id), None) # con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, details='Curso no encontrado')
    return curso

#CRUD: Update (Actualizar/Modificar) PUT: Modificaremos un recurso que coincida con el ID que mandemos
@app.put('/cursos/{curso_id}', response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso = next ((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del arrray devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail='Curso no encontrado')
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso) # Buscamos el índice exacto donde esta el curso en nuestra lista (db)
    cursos_db[index] = curso_actualizado
    return curso_actualizado

#CRUD: Delete (borrado/baja) DELETE: Eliminaremos un recurso que coincida con el ID que mandamos

@app.delete('/cursos/{curso_id}', response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next ((curso for curso in cursos_db if curso.id), None) # con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, details='Curso no encontrado')
    cursos_db.remove(curso)
    return curso