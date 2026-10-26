"""Tests unitaires de la recherche d'une competition."""

from datetime import datetime

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
