from nodos.inDoc import inDoc
from nodos.requestFinal import requestFinal
from nodos.searchDoc import searchDoc
from nodos.utilDoc import utilDoc

if __name__ == "__main__":
    pregunta = "¿Sabes como contactar con Antonio Moreno?"
    respuesta = inDoc(pregunta)
    print(respuesta["inDoc"])

    result = searchDoc(respuesta, pregunta)
    print(result)

    result2 = utilDoc(result, pregunta)
    print(f"Resultado final: {result2}")

    result3 = requestFinal(pregunta, result2, result)
    print(f"Respuesta Final: {result3}")
