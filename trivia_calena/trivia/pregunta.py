"""datos + comportamiento (comprobar una opción)."""

from dataclasses import dataclass

from .constantes import OPCIONES_POR_PREGUNTA


@dataclass(frozen=True)
class Pregunta:
    id: int
    enunciado: str
    opciones: tuple
    correcta: int  # posición (0 a 3) de la opción correcta

    def __post_init__(self):
        if not self.enunciado.strip():
            raise ValueError(f"La pregunta {self.id} no tiene enunciado.")
        if len(self.opciones) != OPCIONES_POR_PREGUNTA:
            raise ValueError(
                f"La pregunta {self.id} debe tener {OPCIONES_POR_PREGUNTA} opciones."
            )
        if not 0 <= self.correcta < len(self.opciones):
            raise ValueError(f"La pregunta {self.id} tiene una posición correcta inválida.")

    def es_correcta(self, opcion: int) -> bool:
        """True si la posición elegida es la respuesta correcta."""
        return opcion == self.correcta

    @classmethod
    def desde_dict(cls, datos: dict) -> "Pregunta":
        """Crea una Pregunta a partir de un registro del JSON."""
        return cls(
            id=datos["id"],
            enunciado=datos["enunciado"],
            opciones=tuple(datos["opciones"]),
            correcta=datos["correcta"],
        )
