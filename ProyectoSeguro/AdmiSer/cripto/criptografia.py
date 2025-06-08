# utils/criptografia.py
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def generar_llave_privada():
    private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
    return private_key

def generar_llave_publica(llave_privada):
    return llave_privada.public_key()

def convertir_llave_privada_bytes(llave_privada):
    return llave_privada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

def convertir_llave_publica_bytes(llave_publica):
    return llave_publica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def cifrar_llave_privada(llave_privada_pem, password):
    password_bytes = password.encode('utf-8')
    salt = os.urandom(16)  # Generar salt de 16 bytes
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b'handshake data'
    ).derive(password_bytes)
    iv = os.urandom(16)  # IV de 16 bytes para AES CTR
    aes_cipher = Cipher(algorithms.AES(derived_key), modes.CTR(iv))
    encryptor = aes_cipher.encryptor()
    llave_privada_cifrada = encryptor.update(llave_privada_pem) + encryptor.finalize()
    
    # Codificar el IV y salt a base64 para almacenarlos
    iv_base64 = base64.b64encode(iv).decode('utf-8')
    salt_base64 = base64.b64encode(salt).decode('utf-8')
    
    return llave_privada_cifrada, iv_base64, salt_base64


def descifrar_llave_privada(private_key_cifrada_base64, password, iv_base64, salt_base64):
    # Decodificar IV y salt desde base64
    iv = base64.b64decode(iv_base64)
    salt=base64.b64decode(salt_base64)

    # Derivar la llave AES de la contraseña y salt usando HKDF
    password_bytes = password.encode('utf-8')
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b'handshake data',
        backend=default_backend()
    ).derive(password_bytes)
    
    print(f"derived_key: {derived_key}")

    # Configuración del cifrado AES en modo CTR
    aes_cipher = Cipher(algorithms.AES(derived_key), modes.CTR(iv), backend=default_backend())
    decryptor = aes_cipher.decryptor()
    # Decodificar la clave privada cifrada desde base64
    private_key_cifrada = base64.b64decode(private_key_cifrada_base64)
    
    # Descifrar la clave privada
    private_key_pem = decryptor.update(private_key_cifrada) + decryptor.finalize()

    # Cargar la clave privada PEM
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,  # No hay password en el PEM
        backend=default_backend()
    )
    return private_key
