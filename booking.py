"""Regles metier de l'achat de places."""


def parse_places(value):
    """Convertit la saisie en entier, ou retourne None si elle est invalide."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def validate_purchase(club, competition, places):
    """Retourne un message d'erreur, ou None si l'achat est valide."""
    if places < 1:
        return 'Sorry, you must book at least one place.'
    return None
