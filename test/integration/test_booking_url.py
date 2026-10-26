"""Tests d'integration de l'acces a la page de reservation."""


def test_acces_page_reservation_valide(client):
    response = client.get('/book/Spring Festival/Simply Lift')

    assert response.status_code == 200
    assert b'Spring Festival' in response.data
    assert b'Places available: 25' in response.data


def test_club_inconnu_dans_l_url_ne_provoque_pas_d_erreur_serveur(client):
    response = client.get('/book/Spring Festival/Fake', follow_redirects=True)

    assert response.status_code == 200
    assert b'does not exist' in response.data


def test_competition_inconnue_dans_l_url_ne_provoque_pas_d_erreur_serveur(client):
    response = client.get('/book/Fake/Simply Lift', follow_redirects=True)

    assert response.status_code == 200
    assert b'does not exist' in response.data


def test_club_et_competition_inconnus_ne_provoquent_pas_d_erreur_serveur(client):
    response = client.get('/book/Fake/Fake', follow_redirects=True)

    assert response.status_code == 200
    assert b'does not exist' in response.data
