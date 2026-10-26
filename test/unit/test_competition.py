"""Tests unitaires de la recherche d'une competition."""

from competition import find_by_name


def test_find_by_name_trouve_la_competition():
    competitions = [
        {'name': 'Spring Festival'},
        {'name': 'Fall Classic'},
    ]

    assert find_by_name(competitions, 'Fall Classic') == {'name': 'Fall Classic'}


def test_find_by_name_inconnu_retourne_none():
    competitions = [{'name': 'Spring Festival'}]

    assert find_by_name(competitions, 'Fake') is None
