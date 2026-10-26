import pytest

import server


@pytest.fixture
def client():
    """Client Flask : simule des requêtes HTTP sans lancer de serveur."""
    server.app.config['TESTING'] = True
    with server.app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def donnees_reinitialisees():
    """Recharge clubs.json et competitions.json avant chaque test.

    L'application garde ses donnees en memoire (variables globales) : sans ce
    rechargement, un achat effectue dans un test modifierait les suivants.
    """
    server.clubs = server.loadClubs()
    server.competitions = server.loadCompetitions()
    yield
