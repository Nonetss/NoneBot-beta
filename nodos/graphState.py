from typing import List

from typing_extensions import TypedDict


class GraphState(TypedDict):
    question: str
    generation: str
    doc: List[str]
