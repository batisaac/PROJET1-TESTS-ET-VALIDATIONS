"""Tests d'integration de la connexion via /showSummary."""


def test_connexion_email_valide(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})

    assert response.status_code == 200
    assert b'Welcome, john@simplylift.co' in response.data


def test_connexion_email_inconnu_ne_provoque_pas_d_erreur_serveur(client):
    response = client.post('/showSummary', data={'email': 'inconnu@club.com'})

    assert response.status_code == 200
    assert b'not registered' in response.data


def test_connexion_champ_email_absent_ne_provoque_pas_d_erreur_serveur(client):
    response = client.post('/showSummary', data={})

    assert response.status_code == 200
    assert b'not registered' in response.data


def test_connexion_email_vide_ne_provoque_pas_d_erreur_serveur(client):
    response = client.post('/showSummary', data={'email': '   '})

    assert response.status_code == 200
    assert b'not registered' in response.data
