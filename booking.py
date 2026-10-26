"""Regles metier de l'achat de places."""

from club import MAX_PLACES


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
    if places > int(competition['numberOfPlaces']):
        return 'Sorry, there are not enough places available.'
    if places > MAX_PLACES:
        return (
            f'Sorry, you cannot book more than {MAX_PLACES} places '
            'per competition.'
        )
    return None
