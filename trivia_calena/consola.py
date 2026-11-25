"""Interfaz de consola PROVISIONAL comprobar que la lógica funciona antes de hacer la interfaz gráfica. consola.py
"""

from trivia.banco import ErrorBanco, cargar_preguntas
from trivia.partida import Partida
from trivia.validaciones import AliasInvalido

LETRAS = "ABCD"


def pedir_alias(preguntas) -> Partida:
    while True:
        texto = input("Alias: ")
        try:
            return Partida(texto, preguntas)
        except AliasInvalido as error:
            print(f"  ✗ {error}")


def pedir_opcion() -> int:
    while True:
        texto = input("Tu respuesta (A/B/C/D): ").strip().upper()
        if len(texto) == 1 and texto in LETRAS:
            return LETRAS.index(texto)
        print(" Selecciona A, B, C o D antes de continuar.")


def jugar(preguntas) -> None:
    partida = pedir_alias(preguntas)
    while not partida.terminada:
        pregunta = partida.pregunta_actual
        print(f"\nPregunta {partida.numero_actual} de {partida.total}")
        print(pregunta.enunciado)
        for letra, opcion in zip(LETRAS, pregunta.opciones):
            print(f"  {letra}) {opcion}")
        if partida.responder(pedir_opcion()):
            print(" ¡Correcto! +10 puntos")
        else:
            correcta = pregunta.opciones[pregunta.correcta]
            print(f" Incorrecto. La respuesta era: {correcta}")
        partida.siguiente()
    r = partida.resumen()
    print("\n=== Resultado ===")
    print(f"Jugador: {r['alias']}")
    print(f"Aciertos: {r['aciertos']}  Errores: {r['errores']}")
    print(f"Puntaje: {r['puntaje']} / {partida.puntaje_maximo}")


def main() -> None:
    print("=== TRIVIA CALEÑA ===")
    try:
        preguntas = cargar_preguntas()
    except ErrorBanco as error:
        print(f"Error: {error}")
        return
    while True:
        jugar(preguntas)
        if input("\n¿Jugar de nuevo? (s/n): ").strip().lower() != "s":
            break


if __name__ == "__main__":
    main()
