"""Tests d'integration de l'achat de places."""

import pytest

DONNEES_VALIDES = {
    'club': 'Simply Lift',
    'competition': 'Spring Festival',
    'places': '1',
}


def test_achat_valide_debute_le_stock(client):
    response = client.post('/purchasePlaces', data=DONNEES_VALIDES)

    assert response.status_code == 200
    assert b'Number of Places: 24' in response.data


def test_competition_inconnue_ne_provoque_pas_d_erreur_serveur(client):
    data = dict(DONNEES_VALIDES, competition='Fake')

    response = client.post('/purchasePlaces', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'does not exist' in response.data


def test_club_inconnu_ne_provoque_pas_d_erreur_serveur(client):
    data = dict(DONNEES_VALIDES, club='Fake')

    response = client.post('/purchasePlaces', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'does not exist' in response.data


def test_champ_places_absent_ne_provoque_pas_d_erreur_serveur(client):
    data = {
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
    }

    response = client.post('/purchasePlaces', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'invalid' in response.data


def test_places_non_numerique_ne_provoque_pas_d_erreur_serveur(client):
    data = dict(DONNEES_VALIDES, places='abc')

    response = client.post('/purchasePlaces', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'invalid' in response.data


@pytest.mark.parametrize('places', ['0', '-5'])
def test_places_non_positives_refusees(client, places):
    data = dict(DONNEES_VALIDES, places=places)

    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200
    assert b'at least one place' in response.data
    assert b'Number of Places: 25' in response.data
