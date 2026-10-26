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


def load_clubs():
    with open(CLUBS_FILE, encoding='utf-8') as fichier:
        return json.load(fichier)['clubs']


def load_competitions():
    with open(COMPETITIONS_FILE, encoding='utf-8') as fichier:
        return json.load(fichier)['competitions']
