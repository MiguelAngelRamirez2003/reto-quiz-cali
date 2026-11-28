import unittest

from src.modelos import Partida, Pregunta, validar_alias


def crear_partida():
    preguntas = [Pregunta(i, f"Pregunta {i}", ["a", "b", "c", "d"], 1) for i in range(3)]
    return Partida("Luna", preguntas)


class TestPartida(unittest.TestCase):
    def test_u1_respuesta_correcta_suma_10(self):
        p = crear_partida()
        p.responder(1)
        self.assertEqual(p.aciertos, 1)
        self.assertEqual(p.puntaje, 10)

    def test_u2_respuesta_incorrecta_no_suma(self):
        p = crear_partida()
        p.responder(0)
        self.assertEqual(p.aciertos, 0)
        self.assertEqual(p.puntaje, 0)

    def test_u3_misma_respuesta_dos_veces_cuenta_una(self):
        p = crear_partida()
        p.responder(1)
        p.responder(1)
        self.assertEqual(p.aciertos, 1)
        self.assertEqual(p.puntaje, 10)

    def test_alias(self):
        self.assertIsNone(validar_alias("   "))
        self.assertIsNone(validar_alias("a"))
        self.assertEqual(validar_alias("  Luna "), "Luna")


if __name__ == "__main__":
    unittest.main()
