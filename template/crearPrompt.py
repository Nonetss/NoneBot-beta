import yaml
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate


class CrearPrompt:
    """
    Clase para generar prompts a partir de un archivo YAML con mensajes del sistema.
    La ruta del archivo YAML es fija.
    """

    RUTA_YAML = "template/prompts.yaml"

    def __init__(self):
        """Carga el archivo YAML con los prompts al iniciar la clase."""
        self.prompts = self._cargar_prompts()

    def _cargar_prompts(self) -> dict:
        """Carga los prompts desde el archivo YAML definido en la ruta fija."""
        try:
            with open(self.RUTA_YAML, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"❌ Error al cargar el archivo YAML: {e}")
            return {}

    def generar_prompt(
        self, nombre_prompt: str, prompt_humano: str
    ) -> ChatPromptTemplate:
        """
        Genera un template de prompt basado en el nombre especificado en el archivo YAML.
        """
        if nombre_prompt not in self.prompts:
            raise ValueError(
                f"❌ El prompt '{nombre_prompt}' no fue encontrado en el archivo YAML."
            )

        prompt_sistema = self.prompts[nombre_prompt]["prompt_sistema"]
        formateado = self.prompts[nombre_prompt].get("formateado", False)

        # Crear el prompt
        prompt = ChatPromptTemplate(
            [
                SystemMessage(content=prompt_sistema),
                HumanMessage(content=prompt_humano),
            ]
        )

        return (prompt.format_prompt(), formateado)
