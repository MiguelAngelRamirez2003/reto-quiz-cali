"""Validaciones de entrada."""

from .constantes import ALIAS_MAX, ALIAS_MIN


class AliasInvalido(ValueError):
    """El alias no cumple las reglas; el mensaje se puede mostrar al usuario."""


def validar_alias(texto: str) -> str:
    """Quita espacios al inicio y al final y devuelve el alias limpio.

    Lanza AliasInvalido con un mensaje claro si queda vacío o si
    su longitud no está entre ALIAS_MIN y ALIAS_MAX caracteres."""
    alias = (texto or "").strip()
    if not alias:
        raise AliasInvalido("Escribe un alias: no puede estar vacío ni ser solo espacios.")
    if len(alias) < ALIAS_MIN:
        raise AliasInvalido(f"El alias debe tener al menos {ALIAS_MIN} caracteres.")
    if len(alias) > ALIAS_MAX:
        raise AliasInvalido(f"El alias puede tener máximo {ALIAS_MAX} caracteres.")
    return alias
