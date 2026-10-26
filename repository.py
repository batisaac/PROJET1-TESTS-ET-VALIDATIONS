"""Acces aux donnees persistees dans les fichiers JSON.

Les chemins sont construits a partir de l'emplacement de ce fichier :
l'application fonctionne donc quel que soit le repertoire depuis lequel
elle est lancee (corrige B18).
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CLUBS_FILE = BASE_DIR / 'clubs.json'
COMPETITIONS_FILE = BASE_DIR / 'competitions.json'


def load_clubs(path=None):
    with open(path or CLUBS_FILE, encoding='utf-8') as fichier:
        return json.load(fichier)['clubs']


def load_competitions(path=None):
    with open(path or COMPETITIONS_FILE, encoding='utf-8') as fichier:
        return json.load(fichier)['competitions']


def save_clubs(clubs, path=None):
    """Ecrit la liste des clubs dans le fichier JSON (atomiquement)."""
    _write({'clubs': clubs}, path or CLUBS_FILE)


def save_competitions(competitions, path=None):
    """Ecrit la liste des competitions dans le fichier JSON."""
    _write({'competitions': competitions}, path or COMPETITIONS_FILE)


def _write(data, path):
    path = Path(path)
    temporaire = path.with_name(path.name + '.tmp')
    with open(temporaire, 'w', encoding='utf-8') as fichier:
        json.dump(data, fichier, indent=4, ensure_ascii=False)
    temporaire.replace(path)
