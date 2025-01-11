import sys

from langchain_chroma import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings

# Cargar el modelo de embeddings
try:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
except Exception as e:
    print(f"Error al cargar el modelo de embeddings: {e}")
    sys.exit(1)

# Conectar con la base de datos existente
try:
    db = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings,
        collection_name="NoneBot_info",
    )
except Exception as e:
    print(f"Error al conectar con ChromaDB: {e}")
    sys.exit(1)


# Función para realizar la búsqueda
def buscar_embeding(query, top_k=2):
    try:
        # Obtener los resultados más similares a la consulta
        resultados = db.similarity_search(query, k=top_k)

        # Mostrar resultados
        if resultados:
            return {"question": query, "document": resultados}
        else:
            return {"question": query, "document": "no"}

    except Exception as e:
        print(f"Error al realizar la búsqueda: {e}")


# Ejemplo de búsqueda
consulta = "NoneNotes"
buscar_embeding(consulta)
