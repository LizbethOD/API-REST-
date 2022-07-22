from fastapi import FastAPI

import sqlite3 
# Permite generar una lista
from typing import List
# Permite validar 
from pydantic import BaseModel

class Respuesta(BaseModel):
    message: str

class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str

app = FastAPI()


@app.get("/", response_model=Respuesta)
async def index():
    return {"message": "API-REST"}

@app.get("/clientes/", response_model=List[Cliente])
async def clientes():
    with sqlite3.connect('/sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes")
        response = cursor.fetchall()
        return response 

@app.get("/clientes/{id}", response_model=List[Cliente])
async def clientes(id: int):
    # Conexion a una BD cierra autometicamenre el archivo que se utilice
    with sqlite3.connect('/sql/clientes.sqlite') as connection:
        connection.row_factory=sqlite3.Row
        # Cursor para realizar las operaciones en la BD
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes where id_cliente={}".format(int(id)))
        # Ordena los formatos en json
        response = cursor.fetchall()
        return response

@app.post("/clientes/", response_model=Respuesta)
async def clientes(nombre: str, email: str):
    with sqlite3.connect('/sql/clientes.sqlite') as connection:
        connection.row_factory=sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("INSERT INTO clientes (nombre,email) values ('{}','{}');". format(nombre,email))
        return {"message":"Nuevo cliente agregado"}
        
@app.put("/clientes/", response_model=Respuesta)
async def clientes( id: int, nombre: str, email: str):
    with sqlite3.connect('/sql/clientes.sqlite') as connection:
        connection.row_factory=sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("UPDATE clientes SET nombre='{}', email='{}' WHERE id_cliente='{}' ;". format(nombre,email,id))
        return {"message":"Actualizacion de cliente realizada"}
        
@app.delete("/clientes/", response_model=Respuesta)
async def clientes( id: int):
    with sqlite3.connect('/sql/clientes.sqlite') as connection:
        connection.row_factory=sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente='{}' ;". format(id))
        return {"message":"Eliminacion de cliente realizada"}