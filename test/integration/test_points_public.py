"""Tests d'integration du tableau public des points (phase 2)."""


def test_tableau_public_accessible_sans_connexion(client):
    response = client.get('/points')

    assert response.status_code == 200


def test_tableau_public_affiche_tous_les_clubs_et_leurs_points(client):
    response = client.get('/points')

    assert b'Simply Lift' in response.data
    assert b'Iron Temple' in response.data
    assert b'She Lifts' in response.data
    assert b'<td>13</td>' in response.data
    assert b'<td>4</td>' in response.data
    assert b'<td>12</td>' in response.data
    assert b'john@simplylift.co' not in response.data
