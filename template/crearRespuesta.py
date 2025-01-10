from langchain_core.output_parsers import JsonOutputParser

from modelo.llama import llm
from template.utils.normaliza_text import normalizar_texto


class CrearRespuesta:
    """
    Clase para generar respuestas a partir de un prompt usando LLM.
    Utiliza JsonOutputParser para asegurar la salida en formato JSON.
    """

    def __init__(self):
        self.json_parser = JsonOutputParser()

    def generar_respuesta(self, prompt):
        """
        Genera una respuesta del modelo LLM usando un prompt ya generado y retorna un JSON válido.
        - prompt: Prompt ya generado con `ChatPromptTemplate`.
        - formateado: Indica si se debe normalizar toda la respuesta o no.
        """
        formateado = prompt[1]
        prompt = prompt[0]

        try:
            # ✅ Invocar el modelo con el prompt generado
            respuesta_raw = llm.invoke(prompt)

            # ✅ Parsear la respuesta a JSON usando JsonOutputParser
            respuesta_json = self.json_parser.parse(respuesta_raw)

            # ✅ Si se solicita formatear, normalizar cada valor de texto del JSON
            if formateado:
                respuesta_json = {
                    key: normalizar_texto(value) if isinstance(value, str) else value
                    for key, value in respuesta_json.items()
                }

            # ✅ Devolver el resultado en formato JSON
            return respuesta_json

        except Exception as e:
            print(f"❌ Error al procesar la respuesta: {e}")
