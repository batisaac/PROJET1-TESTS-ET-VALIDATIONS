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
    available = int(competition['numberOfPlaces'])
    if available == 0:
        return 'Sorry, this competition is full.'
    if places > available:
        return 'Sorry, there are not enough places available.'
    if places > MAX_PLACES:
        return (
            f'Sorry, you cannot book more than {MAX_PLACES} places '
            'per competition.'
        )
    if places > int(club['points']):
        return 'Sorry, you do not have enough points.'
    return None


def confirmation_message(places):
    """Message de confirmation indiquant le nombre de places reservees."""
    suffix = 's' if places > 1 else ''
    return f'Great-booking complete! You have booked {places} place{suffix}.'
