"""Tests d'integration de l'authentification et de la deconnexion."""

import server
from competition import find_by_name


def test_reservation_refusee_sans_session(client):
    response = client.get('/book/Spring Festival/Simply Lift')

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/')


def test_achat_refuse_sans_session(client):
    data = {
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '1',
    }

    response = client.post('/purchasePlaces', data=data)

    competition = find_by_name(server.competitions, 'Spring Festival')

    assert response.status_code == 302
    assert competition['numberOfPlaces'] == '25'


def test_reservation_pour_un_autre_club_refusee(connecte):
    client = connecte()

    response = client.get('/book/Spring Festival/Iron Temple')

    assert response.status_code == 302


def test_achat_pour_un_autre_club_refuse(connecte):
    client = connecte()
    data = {
        'club': 'Iron Temple',
        'competition': 'Spring Festival',
        'places': '1',
    }

    response = client.post('/purchasePlaces', data=data)

    competition = find_by_name(server.competitions, 'Spring Festival')

    assert response.status_code == 302
    assert competition['numberOfPlaces'] == '25'


def test_deconnexion_ferme_la_session(connecte):
    client = connecte()

    assert client.get('/book/Spring Festival/Simply Lift').status_code == 200

    client.get('/logout')

    assert client.get('/book/Spring Festival/Simply Lift').status_code == 302


def test_cle_secrete_n_est_plus_en_dur():
    assert server.app.secret_key != 'something_special'
    assert len(server.app.secret_key) >= 32
