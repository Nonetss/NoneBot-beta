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
        - prompt: Tupla con el prompt generado y el flag de formateo.
        """
        try:
            # ✅ Desempaquetar claramente el prompt y el flag de formateo
            prompt_text, formateado = prompt

            # ✅ Invocar el modelo con el prompt generado
            respuesta_raw = llm.invoke(prompt_text)

            # ✅ Intentar parsear la respuesta como JSON
            try:
                respuesta_json = self.json_parser.parse(respuesta_raw)
            except Exception as json_error:
                print(
                    f"⚠️ Error al parsear JSON. Procesando respuesta como texto plano."
                )
                respuesta_json = {
                    "error": "Formato no válido",
                    "respuesta_raw": respuesta_raw,
                }
                return respuesta_json

            # ✅ Si se solicita formatear, normalizar cada valor de texto del JSON
            if formateado:
                respuesta_json = {
                    key: normalizar_texto(value) if isinstance(value, str) else value
                    for key, value in respuesta_json.items()
                }

            # ✅ Devolver el resultado en formato JSON
            return respuesta_json

        except Exception as e:
            print(f"❌ Error general al procesar la respuesta: {e}")
            return {"error": str(e)}
