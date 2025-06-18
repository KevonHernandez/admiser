#!/bin/bash

ARCHIVO_ENCRIPTADO="credenciales.enc"
RUTA_ENV="./ProyectoSeguro/.env"

limpiar() {
    unset contrasena
    unset CONTENIDO_ENV
    history -c
}

if [ ! -f "$ARCHIVO_ENCRIPTADO" ]; then
    echo "Error: No se encuentra $ARCHIVO_ENCRIPTADO"
    exit 1
fi

# Solicitar contraseña
stty -echo
printf "Contraseña para desencriptar $ARCHIVO_ENCRIPTADO: "
read -r contrasena
stty echo
printf "\n"

# Desencriptar archivo
if ! CONTENIDO_ENV=$(openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 -salt \
    -in "$ARCHIVO_ENCRIPTADO" -pass pass:"$contrasena" 2>/dev/null); then
    echo "Error: Contraseña incorrecta o archivo corrupto"
    limpiar
    exit 1
fi
unset contrasena

# Guardar .env en la ruta que docker-compose necesita
echo "$CONTENIDO_ENV" > "$RUTA_ENV"

# Exportar variables para uso inmediato si se desea
export $(grep -v '^#' "$RUTA_ENV" | xargs)

# Validación rápida
if [ -z "$SECRET_KEY" ] || [ -z "$DB_NAME" ]; then
    echo "Error: Variables no cargadas correctamente"
    limpiar
    exit 1
fi

# Iniciar contenedores
echo "Levantando servicios con Docker..."
docker compose down
docker compose up --build

# Limpieza opcional del entorno y variables
limpiar
