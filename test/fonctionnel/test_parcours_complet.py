"""Tests fonctionnels : parcours complets de l'application."""

import server
from competition import find_by_name

SIMPLY_LIFT = {'email': 'john@simplylift.co'}


def acheter(client, competition, places):
    return client.post(
        '/purchasePlaces',
        data={
            'club': 'Simply Lift',
            'competition': competition,
            'places': str(places),
        },
        follow_redirects=True,
    )


def test_parcours_connexion_achat_et_consultation_publique(client):
    future = find_by_name(server.competitions, 'Spring Festival')
    future['date'] = '2999-01-01 10:00:00'

    response = client.post('/showSummary', data=SIMPLY_LIFT)
    assert b'Spring Festival' in response.data

    response = client.get('/book/Spring Festival/Simply Lift')
    assert b'Places available: 25' in response.data

    response = acheter(client, 'Spring Festival', 2)
    assert b'Great-booking complete!' in response.data
    assert b'Points available: 11' in response.data

    client.get('/logout')
    response = client.get('/points')
    assert response.status_code == 200
    assert b'<td>11</td>' in response.data


def test_parcours_limite_de_douze_places_par_achat(client):
    client.post('/showSummary', data=SIMPLY_LIFT)

    response = acheter(client, 'Spring Festival', 13)
    assert b'more than 12 places' in response.data

    response = acheter(client, 'Spring Festival', 12)
    assert b'Great-booking complete!' in response.data
    assert b'Points available: 1' in response.data

    response = acheter(client, 'Spring Festival', 1)
    assert b'Great-booking complete!' in response.data
    assert b'Points available: 0' in response.data


def test_parcours_stock_epuise_puis_refus(client):
    competition = find_by_name(server.competitions, 'Fall Classic')
    competition['numberOfPlaces'] = '1'
    client.post('/showSummary', data=SIMPLY_LIFT)

    response = acheter(client, 'Fall Classic', 1)
    assert b'Great-booking complete!' in response.data

    response = acheter(client, 'Fall Classic', 1)
    assert b'competition is full' in response.data
    assert b'Points available: 12' in response.data
