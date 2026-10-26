"""Logique metier des competitions."""

from datetime import datetime

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def find_by_name(competitions, name):
    """Retourne la competition dont le nom correspond, sinon None."""
    return next((c for c in competitions if c['name'] == name), None)


def upcoming(competitions, maintenant=None):
    """Retourne les competitions a venir (date invalide : conservee)."""
    maintenant = maintenant or datetime.now()
    resultat = []
    for competition in competitions:
        try:
            date = datetime.strptime(competition['date'], DATE_FORMAT)
        except (KeyError, ValueError):
            resultat.append(competition)
            continue
        if date >= maintenant:
            resultat.append(competition)
    return resultat
