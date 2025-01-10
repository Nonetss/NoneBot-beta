import json
import os
import sys

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings

from embeding.utils.leer_archivos import leer_archivos

# Definimos los directorios
directorio = "embeding/info"
persist_directory = "./chroma_db"
archivos_guardados_path = "embeding/archivos_guardados.json"
archivos_guardados = {}

# Comprobamos que el directorio donde se guarda la info exista
if not os.path.isdir(directorio):
    print("El directorio donde se guarda la info no existe.")
    sys.exit(1)

# Cargar el modelo de embeddings de Ollama
try:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
except Exception as e:
    print(f"Error al cargar el modelo de embeddings: {e}")
    sys.exit(1)

# Cargar la base de datos de ChromaDB
try:
    db = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name="NoneBot_info",
    )
except Exception as e:
    print(f"Error al conectar con ChromaDB: {e}")
    sys.exit(1)

# Intentar cargar el archivo de los archivos guardados
if os.path.exists(archivos_guardados_path):
    try:
        with open(archivos_guardados_path, "r", encoding="utf-8") as f:
            archivos_guardados = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error al leer {archivos_guardados_path}: {e}")

# Configuración del splitter con verificación de `tiktoken`
try:
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=500, chunk_overlap=50
    )
except ImportError:
    print(
        "El paquete `tiktoken` no está instalado. Instálalo con: `pip install tiktoken`."
    )
    sys.exit(1)

# ✅ Ejecutar la función y mostrar resultados usando los argumentos correctos
doc = leer_archivos(
    directorio, text_splitter, archivos_guardados, archivos_guardados_path
)

if doc:
    try:
        # Preparar los textos y metadata para añadirlos a la base de datos
        textos = [documento.page_content for documento in doc]
        metadata = [documento.metadata for documento in doc]

        # Generar los IDs usando la clave correcta
        ids = [
            f"{documento.metadata['hash_document']}_{documento.metadata['fragment_index']}"
            for documento in doc
        ]

        # ✅ Eliminar los vectores antiguos usando `previous_hash`
        with open(archivos_guardados_path, "r", encoding="utf-8") as f:
            archivos_guardados = json.load(f)

        # Recorrer los archivos y eliminar los vectores previos si existen
        for file, data in archivos_guardados.items():
            previous_hash = data.get("previous_hash")
            if previous_hash:  # Solo eliminar si hay un hash anterior
                db.delete(where={"hash": previous_hash})
                print(f"🗑️ Eliminado documento con hash anterior: {previous_hash}")

        # ✅ Agregar documentos actualizados a la base de datos Chroma
        db.add_texts(texts=textos, metadata=metadata, ids=ids)

        # Guardar el archivo actualizado después de procesar los documentos
        with open(archivos_guardados_path, "w", encoding="utf-8") as f:
            json.dump(archivos_guardados, f, ensure_ascii=False, indent=4)

        print(f"✅ Se han agregado {len(doc)} fragmentos nuevos o actualizados.")
    except Exception as e:
        print(f"❌ Error al agregar documentos a la colección: {e}")
else:
    print("ℹ️ No se encontraron documentos nuevos o actualizados.")
