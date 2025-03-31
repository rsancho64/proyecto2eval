# Permitir conexiones X11 desde localhost
xhost +local:

# Ejecutar el contenedor
docker run \
    -ti \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    cristian:latest