"""Tests unitaires de la recherche d'une competition."""

from datetime import datetime

import pytest

from competition import find_by_name, upcoming


def test_find_by_name_trouve_la_competition():
    competitions = [
        {'name': 'Spring Festival'},
        {'name': 'Fall Classic'},
    ]

    assert find_by_name(competitions, 'Fall Classic') == {'name': 'Fall Classic'}


def test_find_by_name_inconnu_retourne_none():
    competitions = [{'name': 'Spring Festival'}]

    assert find_by_name(competitions, 'Fake') is None


def test_upcoming_ne_garde_que_les_competitions_a_venir():
    competitions = [
        {'name': 'Passe', 'date': '2020-01-01 10:00:00'},
        {'name': 'Future', 'date': '2999-01-01 10:00:00'},
    ]

    resultat = upcoming(competitions, maintenant=datetime(2026, 1, 1))

    assert [competition['name'] for competition in resultat] == ['Future']


def test_upcoming_garde_une_date_invalide():
    competitions = [{'name': 'Inconnue', 'date': 'pas une date'}]

    resultat = upcoming(competitions, maintenant=datetime(2026, 1, 1))

    assert resultat == competitions


def test_upcoming_garde_la_date_egale_a_maintenant():
    competitions = [{'name': 'Maintenant', 'date': '2026-01-01 10:00:00'}]

    resultat = upcoming(competitions, maintenant=datetime(2026, 1, 1, 10, 0))

    assert resultat == competitions


def test_upcoming_exclut_une_seconde_avant():
    competitions = [{'name': 'Passe', 'date': '2026-01-01 09:59:59'}]

    resultat = upcoming(competitions, maintenant=datetime(2026, 1, 1, 10, 0))

    assert resultat == []


def test_upcoming_liste_vide():
    assert upcoming([], maintenant=datetime(2026, 1, 1)) == []


def test_upcoming_garde_une_competition_sans_date():
    competitions = [{'name': 'Sans date'}]

    resultat = upcoming(competitions, maintenant=datetime(2026, 1, 1))

    assert resultat == competitions


def test_upcoming_conserve_l_ordre():
    competitions = [
        {'name': 'Future 1', 'date': '2999-01-01 10:00:00'},
        {'name': 'Future 2', 'date': '2998-01-01 10:00:00'},
    ]

    resultat = upcoming(competitions, maintenant=datetime(2026, 1, 1))

    assert [competition['name'] for competition in resultat] == [
        'Future 1',
        'Future 2',
    ]


@pytest.mark.parametrize('date', [
    '2026-01-01',
    '01/01/2026 10:00:00',
])
def test_upcoming_garde_les_formats_invalides(date):
    competitions = [{'name': 'Inconnue', 'date': date}]

    resultat = upcoming(competitions, maintenant=datetime(2026, 1, 1))

    assert resultat == competitions
