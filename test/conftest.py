import pytest

import server
from repository import (
    CLUBS_FILE,
    COMPETITIONS_FILE,
    load_clubs,
    load_competitions,
)


@pytest.fixture
def client():
    """Client Flask : simule des requêtes HTTP sans lancer de serveur."""
    server.app.config['TESTING'] = True
    with server.app.test_client() as c:
        yield c


@pytest.fixture
def connecte(client):
    """Connecte le client avec l'email indique (Simply Lift par defaut)."""
    def _connecte(email='john@simplylift.co'):
        client.post('/showSummary', data={'email': email})
        return client

    return _connecte


@pytest.fixture(autouse=True)
def donnees_reinitialisees():
    """Recharge les donnees avant chaque test et restaure les fichiers apres.

    L'application garde ses donnees en memoire (variables globales) : sans ce
    rechargement, un achat effectue dans un test modifierait les suivants.
    Les tests de persistance ecrivent dans les vrais fichiers JSON : on
    sauvegarde donc leur contenu pour le restaurer en fin de test.
    """
    fichiers = (CLUBS_FILE, COMPETITIONS_FILE)
    contenus = {
        chemin: chemin.read_text(encoding='utf-8') for chemin in fichiers
    }
    server.clubs = load_clubs()
    server.competitions = load_competitions()
    yield
    for chemin, contenu in contenus.items():
        chemin.write_text(contenu, encoding='utf-8')
