"""Regles metier de l'achat de places."""


def parse_places(value):
    """Convertit la saisie en entier, ou retourne None si elle est invalide."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
