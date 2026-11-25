"""controla el avance, evalúa respuestas y calcula el puntaje.
Parte logica, para poder probar de forma automática."""

from dataclasses import dataclass

from .constantes import PREGUNTAS_POR_PARTIDA, PUNTOS_POR_ACIERTO
from .validaciones import validar_alias


@dataclass(frozen=True)
class Respuesta:
    opcion: int
    acerto: bool


class Partida:
    def __init__(self, alias: str, preguntas: list, cantidad: int = PREGUNTAS_POR_PARTIDA):
        self.alias = validar_alias(alias)
        if len(preguntas) < cantidad:
            raise ValueError(f"Se necesitan al menos {cantidad} preguntas.")
        self.preguntas = list(preguntas[:cantidad])  # orden fijo
        self._respuestas = {}   # id de pregunta -> Respuesta (cada una se evalúa una sola vez)
        self._indice = 0        # posición de la pregunta actual

    # ---- consulta del estado ----
    @property
    def total(self) -> int:
        return len(self.preguntas)

    @property
    def numero_actual(self) -> int:
        """Número de la pregunta actual para mostrar 'Pregunta 3 de 10'."""
        return min(self._indice + 1, self.total)

    @property
    def terminada(self) -> bool:
        return self._indice >= self.total

    @property
    def pregunta_actual(self):
        return None if self.terminada else self.preguntas[self._indice]

    @property
    def aciertos(self) -> int:
        return sum(1 for r in self._respuestas.values() if r.acerto)

    @property
    def errores(self) -> int:
        return len(self._respuestas) - self.aciertos

    @property
    def puntaje(self) -> int:
        return self.aciertos * PUNTOS_POR_ACIERTO

    @property
    def puntaje_maximo(self) -> int:
        return self.total * PUNTOS_POR_ACIERTO

    # ---- acciones ----
    def responder(self, opcion: int) -> bool:
        """Confirma la opción para la pregunta actual y dice si acertó.
        Si la pregunta ya fue respondida, no se evalúa de nuevo: se devuelve
        el resultado original y el puntaje no cambia."""
        if self.terminada:
            raise RuntimeError("La partida ya terminó.")
        pregunta = self.pregunta_actual
        if pregunta.id in self._respuestas:
            return self._respuestas[pregunta.id].acerto
        if not isinstance(opcion, int) or not 0 <= opcion < len(pregunta.opciones):
            raise ValueError("Selecciona una de las opciones disponibles.")
        acerto = pregunta.es_correcta(opcion)
        self._respuestas[pregunta.id] = Respuesta(opcion, acerto)
        return acerto

    def ya_respondida(self) -> bool:
        pregunta = self.pregunta_actual
        return pregunta is not None and pregunta.id in self._respuestas

    def siguiente(self) -> None:
        """Pasa a la siguiente pregunta, solo si la actual ya se confirmó."""
        if self.terminada:
            return
        if not self.ya_respondida():
            raise RuntimeError("Confirma una respuesta antes de continuar.")
        self._indice += 1

    def resumen(self) -> dict:
        """Resultado calculado a partir de las respuestas de la partida."""
        return {
            "alias": self.alias,
            "aciertos": self.aciertos,
            "errores": self.errores,
            "puntaje": self.puntaje,
        }
