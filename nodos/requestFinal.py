from nodos.inDoc import inDoc
from nodos.searchDoc import searchDoc
from nodos.utilDoc import utilDoc
from template.crearPrompt import CrearPrompt
from template.crearRespuesta import CrearRespuesta


def requestFinal(question, utilDoc, doc):
    promp = CrearPrompt()
    respuesta = CrearRespuesta()

    if utilDoc == "si":

        for document in doc["document"]:
            prompt_document = document.page_content

            # Generar el prompt individualmente
            pregunta = promp.generar_prompt(
                nombre_prompt="requestDoc",
                prompt_humano=question,
                prompt_document=prompt_document,
            )
            result = respuesta.generar_respuesta(pregunta)
            return result

    else:
        pregunta = promp.generar_prompt(
            nombre_prompt="noRequestDoc",
            prompt_humano=question,
        )
        result = respuesta.generar_respuesta(pregunta)
        return result
