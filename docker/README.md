# Docker

# Crear la imagen
'''bash
docker build -t api_rest:10.06.22 .
'''

# Crear un contenedor 
'''bash 
docker run -it -v "$PWD"/code:/home/code --net host --name api_rest -h api_rest api_rest:10.06.22

docker run -it -v /workspace/API-REST/apirest:/home/apirest --net=host --name apirest -h apirest api_rest:v1
'''

# Abrir pytest
python3 -m pytest -v

# Abrir contenedor  
docker start -i ID