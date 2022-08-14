import hashlib  # Importa la libreria hashlib la cual permite generar un hash 
import sqlite3 #Importa Sqlite3
import os # Permite trabajar con rutas y las ajusta de acuerdo al sistema operativo que se utilice 
from typing import List #Los muestra en forma de lista
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials # De forma automatica solicita usuario y contraseña
from pydantic import BaseModel #Valida el formato
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from urllib.request import Request
from urllib import response
from lib2to3.pytree import Base
from typing import Union
from typing_extensions import Self
import hashlib
import sqlite3
import os
import pyrebase


app = FastAPI() # Se encarga de validar que el formato sea igual a de respuesta

firebaseConfig = {
    'apiKey': "AIzaSyBmKYIgQYdvYQl8PMn7bRefAX7P2xkBCN0",
    'authDomain': "api-firebase-e00d5.firebaseapp.com",
    'databaseURL': "https://api-firebase-e00d5-default-rtdb.firebaseio.com",
    'projectId': "api-firebase-e00d5",
    'storageBucket': "api-firebase-e00d5.appspot.com",
    'messagingSenderId': "326342988677",
    'appId': "1:326342988677:web:bb66f9a6e6d5d637fb6aec"
}

firebase = pyrebase.initialize_app(firebaseConfig)

DATABASE_URL = os.path.join("sql/usuarios.sqlite")
security = HTTPBasic() # Solicita a la API usuario y contraseña
securityBearer = HTTPBearer()

class Respuesta(BaseModel):
    message:str

class Cliente(BaseModel):
    id_cliente:int 
    nombre:str 
    email:str

class Usuarios(BaseModel): 
    username: str
    level: int

class ClienteIN(BaseModel):
    nombre: str
    email: str

class registro(BaseModel):
    nombre: str
    email: str

origin = [
    "https://8000-lizbethod-apirest-n3l0fmlt2en.ws-us60.gitpod.io/"
    "https://8080-lizbethod-apirest-n3l0fmlt2en.ws-us60.gitpod.io/templates",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=Respuesta) 
async def index():
    return  {"mensaje":"API REST"}

@app.get(
    "/clientes/", response_model=List[Cliente],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Muestra una lista de clientes", # Se puede observar en la documentacion de la API
    description="Muestra una lista de clientes",
)
async def get_clientes(credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId'] 

        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM clientes')
            response = cursor.fetchall()
            return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.get(
    "/clientes/{id}", response_model=List[Cliente],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Muestra un solo cliente",
    description="Muestra un solo cliente",
)
async def get_cliente(credentials: HTTPAuthorizationCredentials = Depends(securityBearer),id_cliente: int=0):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId'] 

        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor=connection.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id_cliente={}".format(int(id_cliente)))
            response=cursor.fetchall()
            return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.post(  
    "/clientes/", response_model=Respuesta,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Ingresa un nuevo cliente",
    description="Ingresa un nuevo cliente",
)
async def post_cliente(nombre: str, email:str,level: int = Depends(get_current_level)):
    if level == 1:  # Administrador
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
    if level == 1:  # Administrador
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
    if level == 1:  # Administrador
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


@app.get(
    "/clientes/{id_cliente}", response_model=List[Cliente],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Muestra una lista de clientes", # Se puede observar en la documentacion de la API
    description="Muestra una lista de clientes",
)
async def get_clientes(level: int = Depends(get_current_level)):
    if level == 1:  # Administrador
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory=sqlite3.Row
            cursor = connection.cursor() 
            cursor.execute("SELECT id_cliente, nombre, email * FROM clientes where id_cliente = ?",(id_cliente,))
            response = cursor.fetchone()
            if response is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="id_cliente no encontrado",
                    headers={"WWW-Authenticate": "Basic"},
            )
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )