import json
from pathlib import Path

from .pregunta import Pregunta

RUTA_POR_DEFECTO = Path(__file__).resolve().parent.parent / "datos" / "preguntas.json"


class ErrorBanco(Exception):
    """No se pudo leer o interpretar el banco de preguntas."""


def cargar_preguntas(ruta=RUTA_POR_DEFECTO) -> list:
    """Devuelve la lista de Pregunta; lanza ErrorBanco con un mensaje comprensible."""
    try:
        with open(ruta, encoding="utf-8") as archivo:
            registros = json.load(archivo)
        preguntas = [Pregunta.desde_dict(r) for r in registros]
    except FileNotFoundError:
        raise ErrorBanco(f"No se encontró el banco de preguntas: {ruta}")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        raise ErrorBanco(f"El banco de preguntas no es válido: {error}")
    if not preguntas:
        raise ErrorBanco("El banco de preguntas está vacío.")
    return preguntas
