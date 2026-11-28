"""Interfaz grafica con Tkinter. No calcula puntajes: le pregunta a Partida."""
import tkinter as tk
from tkinter import messagebox

from src.modelos import Partida, validar_alias


class App:
    def __init__(self, raiz, preguntas):
        self.raiz = raiz
        self.preguntas = preguntas
        self.partida = None
        self.ultimo_alias = ""
        self.on_enter = lambda: None

        raiz.title("Trivia Caleña")
        raiz.geometry("560x460")
        raiz.minsize(400, 380)
        # La tecla Enter ejecuta la accion principal de la pantalla actual
        raiz.bind("<Return>", lambda e: self.on_enter())
        self.mostrar_inicio()

    def limpiar(self):
        for w in self.raiz.winfo_children():
            w.destroy()

    # ---------------- INICIO ----------------
    def mostrar_inicio(self):
        self.limpiar()
        tk.Label(self.raiz, text="Trivia Caleña", font=("Arial", 22, "bold")).pack(pady=(30, 5))
        tk.Label(self.raiz, text="¿Cuánto sabes de la cultura de Cali?",
                 font=("Arial", 12)).pack(pady=(0, 20))
        tk.Label(self.raiz, text="Alias (2 a 20 caracteres):", font=("Arial", 12)).pack()
        self.entrada = tk.Entry(self.raiz, font=("Arial", 14), justify="center")
        self.entrada.insert(0, self.ultimo_alias)
        self.entrada.pack(pady=5)
        self.entrada.focus()
        self.msg = tk.Label(self.raiz, text="", fg="red", font=("Arial", 11))
        self.msg.pack()
        tk.Button(self.raiz, text="Iniciar partida", font=("Arial", 12),
                  command=self.iniciar).pack(pady=10)
        self.on_enter = self.iniciar

    def iniciar(self):
        alias = validar_alias(self.entrada.get())
        if alias is None:
            self.msg.config(text="Escribe un alias válido de 2 a 20 caracteres.")
            self.entrada.focus()
            return
        self.ultimo_alias = alias
        self.partida = Partida(alias, self.preguntas)
        self.mostrar_pregunta()

    # ---------------- JUEGO ----------------
    def mostrar_pregunta(self):
        self.limpiar()
        p = self.partida.pregunta_actual()
        tk.Label(self.raiz,
                 text=f"Pregunta {self.partida.numero_actual()} de {self.partida.total}",
                 font=("Arial", 11, "bold")).pack(pady=(15, 5))
        tk.Label(self.raiz, text=p.enunciado, font=("Arial", 14),
                 wraplength=480, justify="left").pack(pady=10, padx=20)

        self.eleccion = tk.IntVar(value=-1)  # -1 = nada seleccionado
        self.radios = []
        for i, opcion in enumerate(p.opciones):
            r = tk.Radiobutton(self.raiz, text=opcion, variable=self.eleccion,
                               value=i, font=("Arial", 12), anchor="w",
                               wraplength=450, justify="left")
            r.pack(fill="x", padx=40, pady=2)
            self.radios.append(r)
        self.radios[0].focus()

        self.resultado = tk.Label(self.raiz, text="", font=("Arial", 12, "bold"),
                                  wraplength=480)
        self.resultado.pack(pady=8)
        self.btn_confirmar = tk.Button(self.raiz, text="Confirmar", font=("Arial", 12),
                                       command=self.confirmar)
        self.btn_confirmar.pack(pady=3)
        texto_sig = "Ver resultado" if self.partida.es_ultima() else "Siguiente"
        self.btn_siguiente = tk.Button(self.raiz, text=texto_sig, font=("Arial", 12),
                                       command=self.siguiente, state="disabled")
        self.btn_siguiente.pack(pady=3)
        self.on_enter = self.accion_enter_juego

    def accion_enter_juego(self):
        if self.partida.ya_respondida():
            self.siguiente()
        else:
            self.confirmar()

    def confirmar(self):
        if self.partida.ya_respondida():
            return  # ya evaluada: no se vuelve a contar
        if self.eleccion.get() == -1:
            self.resultado.config(text="Selecciona una opción antes de confirmar.", fg="red")
            return
        acierto = self.partida.responder(self.eleccion.get())
        self.btn_confirmar.config(state="disabled")
        for r in self.radios:
            r.config(state="disabled")
        if acierto:
            self.resultado.config(text="¡Correcto! +10 puntos", fg="green")
        else:
            correcta = self.partida.pregunta_actual().texto_correcto
            self.resultado.config(
                text=f"Incorrecto. La respuesta correcta era: {correcta}", fg="red")
        self.btn_siguiente.config(state="normal")
        self.btn_siguiente.focus()

    def siguiente(self):
        if not self.partida.ya_respondida():
            return
        self.partida.siguiente()
        if self.partida.terminada():
            self.mostrar_final()
        else:
            self.mostrar_pregunta()

    # ---------------- FINAL ----------------
    def mostrar_final(self):
        self.limpiar()
        p = self.partida
        tk.Label(self.raiz, text="¡Partida terminada!", font=("Arial", 20, "bold")).pack(pady=(30, 10))
        tk.Label(self.raiz, text=f"Jugador: {p.alias}", font=("Arial", 13)).pack()
        tk.Label(self.raiz, text=f"Aciertos: {p.aciertos}", font=("Arial", 14)).pack(pady=2)
        tk.Label(self.raiz, text=f"Errores: {p.errores}", font=("Arial", 14)).pack(pady=2)
        tk.Label(self.raiz, text=f"Puntaje: {p.puntaje} / 100",
                 font=("Arial", 16, "bold")).pack(pady=10)
        # Dias 8 y 9: aqui se guardara el resultado y se mostrara la clasificacion.
        btn = tk.Button(self.raiz, text="Jugar de nuevo", font=("Arial", 12),
                        command=self.mostrar_inicio)
        btn.pack(pady=10)
        btn.focus()
        self.on_enter = self.mostrar_inicio


def mostrar_error(titulo, mensaje):
    messagebox.showerror(titulo, mensaje)
