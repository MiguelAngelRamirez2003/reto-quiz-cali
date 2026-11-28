"""Logica del juego: clases Pregunta y Partida. No usa interfaz grafica."""

NUM_PREGUNTAS = 10
PUNTOS_POR_ACIERTO = 10
ALIAS_MIN = 2
ALIAS_MAX = 20


def validar_alias(texto):
    """Devuelve el alias sin espacios en los extremos, o None si no es valido."""
    alias = texto.strip()
    if ALIAS_MIN <= len(alias) <= ALIAS_MAX:
        return alias
    return None


class Pregunta:
    def __init__(self, id, enunciado, opciones, correcta):
        self.id = id
        self.enunciado = enunciado
        self.opciones = opciones
        self.correcta = correcta

    def es_correcta(self, indice_opcion):
        return indice_opcion == self.correcta

    @property
    def texto_correcto(self):
        return self.opciones[self.correcta]


class Partida:
    def __init__(self, alias, preguntas):
        self.alias = alias
        self.preguntas = list(preguntas)
        self.indice = 0          # posicion de la pregunta actual
        self.aciertos = 0
        self.errores = 0
        self._respondida = False  # la pregunta actual ya fue evaluada?
        self._ultimo_acierto = None

    @property
    def total(self):
        return len(self.preguntas)

    @property
    def puntaje(self):
        return self.aciertos * PUNTOS_POR_ACIERTO

    def pregunta_actual(self):
        return self.preguntas[self.indice]

    def numero_actual(self):
        return self.indice + 1

    def es_ultima(self):
        return self.indice == self.total - 1

    def ya_respondida(self):
        return self._respondida

    def responder(self, indice_opcion):
        """Evalua la pregunta actual UNA sola vez.
        Si se llama de nuevo, devuelve el mismo resultado sin volver a sumar."""
        if self._respondida:
            return self._ultimo_acierto
        acierto = self.pregunta_actual().es_correcta(indice_opcion)
        if acierto:
            self.aciertos += 1
        else:
            self.errores += 1
        self._respondida = True
        self._ultimo_acierto = acierto
        return acierto

    def siguiente(self):
        """Pasa a la siguiente pregunta (solo si ya se respondio la actual)."""
        if not self._respondida:
            return
        self.indice += 1
        self._respondida = False
        self._ultimo_acierto = None

    def terminada(self):
        return self.indice >= self.total
