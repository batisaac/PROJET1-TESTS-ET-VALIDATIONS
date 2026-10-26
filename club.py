"""Logique metier des clubs."""

MAX_PLACES = 12


def find_by_email(clubs, email):
    """Retourne le club dont l'email correspond, sinon None."""
    email = (email or '').strip()
    return next((club for club in clubs if club['email'] == email), None)


def find_by_name(clubs, name):
    """Retourne le club dont le nom correspond, sinon None."""
    return next((club for club in clubs if club['name'] == name), None)
