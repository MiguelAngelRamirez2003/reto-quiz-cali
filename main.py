"""Punto de entrada: python main.py"""
import tkinter as tk

from src.almacenamiento import cargar_preguntas
from src.interfaz import App, mostrar_error
from src.modelos import NUM_PREGUNTAS


def main():
    raiz = tk.Tk()
    try:
        preguntas = cargar_preguntas()
    except (OSError, ValueError, KeyError) as error:
        mostrar_error("Error", f"No se pudieron cargar las preguntas:\n{error}")
        raiz.destroy()
        return
    if len(preguntas) < NUM_PREGUNTAS:
        mostrar_error("Error", f"Se necesitan al menos {NUM_PREGUNTAS} preguntas.")
        raiz.destroy()
        return
    App(raiz, preguntas[:NUM_PREGUNTAS])  # las primeras 10, en orden fijo
    raiz.mainloop()


if __name__ == "__main__":
    main()
