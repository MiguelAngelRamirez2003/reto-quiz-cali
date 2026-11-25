"""Pruebas automáticas de la lógica.
python -m unittest discover -s pruebas -v"""

import unittest

from trivia.banco import cargar_preguntas
from trivia.partida import Partida
from trivia.validaciones import AliasInvalido, validar_alias


def nueva_partida() -> Partida:
    return Partida("Luna", cargar_preguntas())


def jugar_todo(partida: Partida, correctas: int) -> None:
    """Responde bien las primeras `correctas` preguntas y mal el resto."""
    for i in range(partida.total):
        p = partida.pregunta_actual
        if i < correctas:
            partida.responder(p.correcta)
        else:
            partida.responder((p.correcta + 1) % 4)
        partida.siguiente()


class PruebasObligatorias(unittest.TestCase):
    def test_U1_respuesta_correcta_suma_10(self):
        partida = nueva_partida()
        partida.responder(partida.pregunta_actual.correcta)
        self.assertEqual(partida.aciertos, 1)
        self.assertEqual(partida.puntaje, 10)

    def test_U2_respuesta_incorrecta_no_suma(self):
        partida = nueva_partida()
        partida.responder((partida.pregunta_actual.correcta + 1) % 4)
        self.assertEqual(partida.aciertos, 0)
        self.assertEqual(partida.puntaje, 0)

    def test_U3_misma_respuesta_dos_veces_cuenta_una_vez(self):
        partida = nueva_partida()
        correcta = partida.pregunta_actual.correcta
        partida.responder(correcta)
        partida.responder(correcta)
        self.assertEqual(partida.aciertos, 1)
        self.assertEqual(partida.puntaje, 10)


class PruebasAdicionales(unittest.TestCase):
    def test_siete_aciertos_tres_errores(self):
        partida = nueva_partida()
        jugar_todo(partida, 7)
        self.assertTrue(partida.terminada)
        self.assertEqual((partida.aciertos, partida.errores, partida.puntaje), (7, 3, 70))

    def test_todo_incorrecto_da_cero(self):
        partida = nueva_partida()
        jugar_todo(partida, 0)
        self.assertEqual((partida.aciertos, partida.errores, partida.puntaje), (0, 10, 0))

    def test_todo_correcto_da_cien(self):
        partida = nueva_partida()
        jugar_todo(partida, 10)
        self.assertEqual(partida.puntaje, 100)

    def test_no_avanza_sin_responder(self):
        partida = nueva_partida()
        with self.assertRaises(RuntimeError):
            partida.siguiente()

    def test_cambiar_respuesta_tras_confirmar_no_afecta(self):
        partida = nueva_partida()
        correcta = partida.pregunta_actual.correcta
        partida.responder((correcta + 1) % 4)      # error
        partida.responder(correcta)                # intento de cambio: se ignora
        self.assertEqual(partida.puntaje, 0)

    def test_partidas_nuevas_son_independientes(self):
        preguntas = cargar_preguntas()
        a = Partida("Ana", preguntas)
        a.responder(a.pregunta_actual.correcta)
        b = Partida("Ana", preguntas)
        self.assertEqual(b.puntaje, 0)

    def test_alias_valido_y_recortado(self):
        self.assertEqual(validar_alias("  Luna  "), "Luna")

    def test_alias_invalido(self):
        for malo in ("", "   ", "a", "x" * 21):
            with self.subTest(alias=malo):
                with self.assertRaises(AliasInvalido):
                    validar_alias(malo)


if __name__ == "__main__":
    unittest.main()
