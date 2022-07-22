import hashlib  # Importa la libreria hashlib la cual permite generar un hash 
import sqlite3 #Importa Sqlite3
import os # Permite trabajar con rutas y las ajusta de acuerdo al sistema operativo que se utilice 
from typing import List #Los muestra en forma de lista

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials # De forma automatica solicita usuario y contraseña
from pydantic import BaseModel #Valida el formato

app = FastAPI() # Se encarga de validar que el formato sea igual a de respuesta

DATABASE_URL = os.path.join("sql/usuarios.sqlite")
security = HTTPBasic() # Solicita a la API usuario y contraseña

class Respuesta(BaseModel):
    message:str

class Cliente(BaseModel):
    id_cliente:int 
    nombre:str 
    email:str

class Usuarios(BaseModel): 
    username: str
    level: int

def get_current_level(credentials: HTTPBasicCredentials = Depends(security)): # Se encarga de recibir los user y password,ademas indica si las contraseñas son correctas
    password_b = hashlib.md5(credentials.password.encode()) # Lo convierte en MD5
    password = password_b.hexdigest() # Lo convierte a BITS
    with sqlite3.connect(DATABASE_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT level FROM usuarios WHERE username = ? and password = ?",
            (credentials.username, password),
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException( 
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
    return user[0]

@app.get("/", response_model=Respuesta) 
async def index():
    return  {"mensaje":"API REST"}

@app.get(
    "/clientes/", response_model=List[Cliente],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Muestra una lista de clientes", # Se puede observar en la documentacion de la API
    description="Muestra una lista de clientes",
)
async def get_clientes(level: int = Depends(get_current_level)):
    if level == 1:  # Administrador
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory=sqlite3.Row
            cursor = connection.cursor() 
            cursor.execute("SELECT * FROM clientes")
            response = cursor.fetchall()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get(
    "/clientes/{id}", response_model=List[Cliente],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Muestra un solo cliente",
    description="Muestra un solo cliente",
)
async def get_cliente(id: int,level: int = Depends(get_current_level)):
    if level == 0:  # Administrador
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory=sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes where id_cliente={}".format(id))
            response = cursor.fetchall()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.post(  
    "/clientes/", response_model=Respuesta,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Ingresa un nuevo cliente",
    description="Ingresa un nuevo cliente",
)
async def post_cliente(nombre: str, email:str,level: int = Depends(get_current_level)):
    if level == 0:  # Administrador
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory=sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("INSERT INTO clientes (nombre, email) values ('{}','{}');".format(nombre,email))
            return {"message":"Nuevo cliente agregado"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.put(  
    "/clientes/", response_model=Respuesta,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Actualiza un cliente", 
    description="Actualiza un cliente",
)
async def put_cliente(id:int, nombre: str, email:str,level: int = Depends(get_current_level)):
    if level == 0:  # Administrador
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory=sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("UPDATE clientes SET nombre='{}', email='{}' WHERE id_cliente={} ;".format(nombre,email,id))
            response = {"message":"Actualizacion de cliente realizada"}
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.delete(  
    "/clientes/", response_model=Respuesta,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Elimina un cliente",
    description="Elimina un cliente",
)
async def delete_cliente(id:int,level: int = Depends(get_current_level)):
    if level == 0:  # Administrador
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory=sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente={};".format(id))
            response = {"message":"Eliminacion de cliente realizada"}
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )