import unicodedata


def normalizar_texto(texto: str) -> str:
    """Convierte un texto a minúsculas y elimina acentos."""
    # Convertir a minúsculas y eliminar acentos
    texto = texto.lower()
    texto = "".join(
        c
        for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    return texto
