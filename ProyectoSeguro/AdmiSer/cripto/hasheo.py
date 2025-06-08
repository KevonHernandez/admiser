import hashlib
import os
import base64

def generar_salt():
    return os.urandom(16)

def hashear_password(password, salt):
    password_bytes = password.encode('utf-8')
    password_con_salt = password_bytes + salt
    hasher = hashlib.sha512()
    hasher.update(password_con_salt)
    hash_resultado = hasher.hexdigest()
    return hash_resultado, salt

def password_valido(password, hash_almacenado, salt_almacenado):
    password_bytes = password.encode('utf-8')
    password_con_salt = password_bytes + salt_almacenado
    hasher = hashlib.sha512()
    hasher.update(password_con_salt)
    hash_resultado = hasher.hexdigest()
    return hash_almacenado == hash_resultado

def convertir_binario_texto64(data_binaria):
    """Convierte datos binarios a Base64 con relleno si es necesario."""
    base64_data = base64.b64encode(data_binaria).decode('utf-8')
    # Asegurarse de que esté correctamente alineado con el relleno
    return base64_data + ('=' * ((4 - len(base64_data) % 4) % 4))

def convertir_texto64_binario(texto64):
    # Añadir el padding de Base64 si es necesario
    padding = len(texto64) % 4
    if padding != 0:
        texto64 += "=" * (4 - padding)  # Agregar el padding necesario
    return base64.b64decode(texto64)
