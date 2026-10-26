"""Tests d'integration de l'achat de places."""

import pytest

import server
from club import find_by_email
from competition import find_by_name
from repository import load_clubs, load_competitions

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


def test_demande_superieure_au_stock_refusee(client):
    competition = find_by_name(server.competitions, 'Fall Classic')
    competition['numberOfPlaces'] = '5'
    data = {
        'club': 'Simply Lift',
        'competition': 'Fall Classic',
        'places': '6',
    }

    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200
    assert b'not enough places' in response.data
    assert b'Number of Places: 5' in response.data


def test_demande_egale_au_stock_acceptee(client):
    competition = find_by_name(server.competitions, 'Fall Classic')
    competition['numberOfPlaces'] = '5'
    data = {
        'club': 'Simply Lift',
        'competition': 'Fall Classic',
        'places': '5',
    }

    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
    assert b'Number of Places: 0' in response.data


def test_demande_superieure_a_12_places_refusee(client):
    data = dict(DONNEES_VALIDES, places='13')

    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200
    assert b'more than 12 places' in response.data
    assert b'Number of Places: 25' in response.data


def test_demande_de_12_places_acceptee(client):
    data = dict(DONNEES_VALIDES, places='12')

    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
    assert b'Number of Places: 13' in response.data


def test_solde_de_points_insuffisant_refuse(client):
    data = {
        'club': 'Iron Temple',
        'competition': 'Spring Festival',
        'places': '5',
    }

    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200
    assert b'do not have enough points' in response.data
    assert b'Number of Places: 25' in response.data
    assert b'Points available: 4' in response.data


def test_achat_debute_les_points_et_confirme_le_nombre(client):
    data = {
        'club': 'Iron Temple',
        'competition': 'Spring Festival',
        'places': '1',
    }

    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200
    assert b'Points available: 3' in response.data
    assert b'You have booked 1 place.' in response.data


def test_concours_complet_refuse(client):
    competition = find_by_name(server.competitions, 'Fall Classic')
    competition['numberOfPlaces'] = '0'
    data = {
        'club': 'Simply Lift',
        'competition': 'Fall Classic',
        'places': '1',
    }

    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200
    assert b'competition is full' in response.data
    assert b'Points available: 13' in response.data


def test_achat_de_deux_places_debute_deux_points(client):
    data = dict(DONNEES_VALIDES, places='2')

    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200
    assert b'Points available: 11' in response.data
    assert b'You have booked 2 places.' in response.data


def test_achat_persiste_les_points_et_le_stock(client):
    response = client.post('/purchasePlaces', data=DONNEES_VALIDES)

    assert response.status_code == 200

    club = find_by_email(load_clubs(), 'john@simplylift.co')
    competition = find_by_name(load_competitions(), 'Spring Festival')

    assert club['points'] == 12
    assert competition['numberOfPlaces'] == 24
