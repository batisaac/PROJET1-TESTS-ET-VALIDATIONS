"""Logique metier des clubs."""

MAX_PLACES = 12


def find_by_email(clubs, email):
    """Retourne le club dont l'email correspond, sinon None."""
    email = (email or '').strip()
    return next((club for club in clubs if club['email'] == email), None)
