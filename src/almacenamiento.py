"""Carga y guardado de datos."""
import json
import os

from src.modelos import Pregunta

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_PREGUNTAS = os.path.join(RAIZ, "data", "preguntas.json")


def cargar_preguntas(ruta=RUTA_PREGUNTAS):
    """Lee el banco de preguntas. Lanza una excepcion si el archivo falla."""
    with open(ruta, encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return [
        Pregunta(d["id"], d["enunciado"], d["opciones"], d["correcta"])
        for d in datos
    ]

# Dias 8 y 9: aqui se agregaran guardar_resultado() y cargar_historial().