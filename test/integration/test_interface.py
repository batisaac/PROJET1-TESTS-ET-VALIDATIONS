"""Tests d'integration de l'interface HTML."""

import server
from competition import find_by_name


def test_welcome_affiche_seulement_les_competitions_a_venir(connecte):
    future = find_by_name(server.competitions, 'Spring Festival')
    future['date'] = '2999-01-01 10:00:00'
    client = connecte()

    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})

    assert b'Spring Festival' in response.data
    assert b'Fall Classic' not in response.data
    assert b'</br>' not in response.data


def test_page_reservation_contient_les_contraintes_html(connecte):
    client = connecte()

    response = client.get('/book/Spring Festival/Simply Lift')

    assert b'id="places"' in response.data
    assert b'min="1"' in response.data
    assert b'max="12"' in response.data
    assert b'id=""' not in response.data


def test_page_accueil_associe_le_label_et_le_champ(client):
    response = client.get('/')

    assert b'id="email"' in response.data
    assert b'id=""' not in response.data


def test_feuille_de_style_est_servie_et_referencee(client):
    """T-I34 : le CSS de la refonte est servi et charge par les pages."""
    response = client.get('/static/css/gudlft.css')

    assert response.status_code == 200
    assert response.mimetype == 'text/css'
    assert b'--rouge' in response.data
    assert b'/static/css/gudlft.css' in client.get('/').data
    assert b'data-testid="login-form"' in client.get('/').data
    assert b'data-testid="points-table"' in client.get('/points').data
