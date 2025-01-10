import json
import os
import sys
from datetime import datetime

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings

# Configurar el directorio donde están los archivos de tu portafolio
directorio = "./info"

# Verificar que el directorio exista
if not os.path.isdir(directorio):
    print(f"El directorio {directorio} no existe.")
    sys.exit(1)

# Cargar el modelo de embeddings de Ollama
try:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
except Exception as e:
    print(f"Error al cargar el modelo de embeddings: {e}")
    sys.exit(1)

# Configurar ChromaDB (sin persist())
persist_directory = "./chroma_db"

try:
    db = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name="portafolio_documents",
    )
except Exception as e:
    print(f"Error al conectar con ChromaDB: {e}")
    sys.exit(1)

# Intentar cargar el archivo de los archivos guardados
archivos_guardados_path = "archivos_guardados.json"
archivos_guardados = {}
if os.path.exists(archivos_guardados_path):
    try:
        with open(archivos_guardados_path, "r", encoding="utf-8") as f:
            archivos_guardados = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error al leer {archivos_guardados_path}: {e}")

# Configurar el text splitter para dividir en fragmentos más pequeños
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # Tamaño del fragmento
    chunk_overlap=50,  # Superposición para mantener contexto
)


# Función para leer y dividir archivos .md en fragmentos
def leer_archivos(directorio):
    documentos = []
    for filename in os.listdir(directorio):
        if filename.endswith(".md"):
            ruta_archivo = os.path.join(directorio, filename)
            try:
                fecha_modificacion = os.path.getmtime(ruta_archivo)
            except OSError as e:
                print(
                    f"Error al obtener la fecha de modificación de {ruta_archivo}: {e}"
                )
                continue

            # Verificar si el archivo ha sido modificado desde la última vez que se guardó
            if (
                filename not in archivos_guardados
                or archivos_guardados[filename] != fecha_modificacion
            ):
                try:
                    with open(ruta_archivo, "r", encoding="utf-8") as file:
                        contenido = file.read()
                        # Dividir el texto en fragmentos usando el splitter
                        fragmentos = text_splitter.split_text(contenido)
                        # Crear un documento para cada fragmento
                        for i, fragmento in enumerate(fragmentos):
                            documentos.append(
                                Document(
                                    page_content=fragmento,
                                    metadata={
                                        "filename": filename,
                                        "last_modified": fecha_modificacion,
                                        "fragment_index": i,
                                    },
                                )
                            )
                    archivos_guardados[filename] = fecha_modificacion
                except Exception as e:
                    print(f"Error al leer el archivo {ruta_archivo}: {e}")
    return documentos


# Leer los archivos nuevos o modificados y crear los documentos
documentos = leer_archivos(directorio)

# Si hay nuevos documentos o documentos modificados, agregarlos a la base de datos
if documentos:
    try:
        textos = [doc.page_content for doc in documentos]
        metadatas = [doc.metadata for doc in documentos]
        ids = [
            f"{doc.metadata['filename']}_frag_{doc.metadata['fragment_index']}"
            for doc in documentos
        ]

        db.add_texts(texts=textos, metadatas=metadatas, ids=ids)

        # ✅ Eliminado: persist() ya no es necesario
        # db.persist()

        # Guardar el estado actualizado de los archivos procesados
        with open(archivos_guardados_path, "w", encoding="utf-8") as f:
            json.dump(archivos_guardados, f, ensure_ascii=False, indent=4)
        print(f"Se han agregado {len(documentos)} fragmentos nuevos o actualizados.")
    except Exception as e:
        print(f"Error al agregar documentos a la colección: {e}")
else:
    print("No se encontraron documentos nuevos o actualizados.")
