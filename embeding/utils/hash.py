import hashlib


def calcular_hash(file):
    # Crear un objeto hash SHA-256
    sha256 = hashlib.sha256()

    # Abrir el archivo en modo binario
    with open(file, "rb") as f:
        # Leer el archivo en bloques para manejar archivos grandes
        for bloque in iter(lambda: f.read(4096), b""):
            sha256.update(bloque)

    # Devolver el hash hexadecimal
    return sha256.hexdigest()
