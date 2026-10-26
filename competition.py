"""Logique metier des competitions."""


def find_by_name(competitions, name):
    """Retourne la competition dont le nom correspond, sinon None."""
    return next((c for c in competitions if c['name'] == name), None)
