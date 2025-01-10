from langchain.memory import ChatMessageHistory
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings

# Inicializar modelo de embeddings y modelo Llama3.2 con el nombre NoneBot
embeddings = OllamaEmbeddings(model="nomic-embed-text")
nonebot = OllamaLLM(model="llama3.2")  # Ahora el modelo se llama NoneBot

# Inicializar memoria para recordar mensajes anteriores
memory = ChatMessageHistory()

# Cargar la base de datos asegurando el nombre de la colección correcto
chroma_db = Chroma(
    embedding_function=embeddings,
    persist_directory="./chroma_db",
    collection_name="portafolio_documents",
)

# Verificar si los documentos realmente están indexados
cantidad_documentos = len(chroma_db.get()["ids"])
print(f"Cantidad de documentos en la base de datos: {cantidad_documentos}")

# Mensaje de bienvenida con la identidad de NoneBot
print("\n💬 Bienvenido al chat con NoneBot, el asistente personal de Antonio.")
print("Escribe 'salir' para terminar la conversación.\n")

# Bucle de conversación interactiva
while True:
    # Recibir la pregunta del usuario
    query = input("🗨️  Tu pregunta: ")

    # Permitir salir del chat
    if query.lower() == "salir":
        print("👋 ¡Hasta luego! Gracias por visitar el portafolio de Antonio.")
        break

    # Guardar la interacción en memoria
    memory.save_context({"input": query}, {"output": ""})

    # Realizar la búsqueda en ChromaDB para encontrar contexto relevante
    resultados = chroma_db.similarity_search(query, k=1)

    contexto_base = (
        "Tu nombre es NoneBot y estás alojado en el portafolio de Antonio Moreno. "
        "Tu función es resolver con precisión y elegancia las dudas de quienes visitan el portafolio. "
        "Responde de forma directa, con un ingenio afilado y un toque sofisticado, sin perder claridad. "
        "Tus respuestas deben ser breves, precisas y con un toque sarcástico cuando sea apropiado. "
        "Utiliza emojis con moderación, solo cuando aporten expresividad al mensaje. 🎯 "
        "Evita presentarte o agradecer constantemente. No hables en primera persona como si fueras Antonio Moreno. "
        "En todo momento, procura dejar a Antonio en buen lugar, ya que muchas de las personas que acceden al portafolio podrían estar interesadas en contratar sus servicios. "
        "Ofrece información exacta, sin especulaciones ni asumir información personal. "
        "Si la información es insuficiente, dilo con estilo e ingenio. 🤖"
    )

    # Construir el prompt incluyendo la memoria y el contexto
    historial = memory.load_memory_variables({})
    memoria_texto = historial.get("history", "")

    if resultados:
        contexto_documento = resultados[0].page_content
        prompt = (
            f"{contexto_base}\n"
            f"Contexto adicional del portafolio: {contexto_documento}\n\n"
            f"Historial de la conversación:\n{memoria_texto}\n"
            f"Pregunta: {query}\nRespuesta:"
        )

        # Generar la respuesta usando NoneBot
        respuesta = nonebot.invoke(prompt)
        print(f"🤖 NoneBot: {respuesta}\n")

        # Actualizar la memoria con la respuesta generada
        memory.save_context({"input": query}, {"output": respuesta})

    else:
        print("❌ No se encontró información relevante en el portafolio de Antonio.\n")
