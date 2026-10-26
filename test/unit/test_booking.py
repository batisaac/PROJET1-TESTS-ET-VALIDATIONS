"""Tests unitaires des regles d'achat de places."""

import pytest

from booking import parse_places, validate_purchase

CLUB = {'points': '13'}
COMPETITION = {'numberOfPlaces': '25'}


def test_parse_places_entier_valide():
    assert parse_places('3') == 3


def test_parse_places_accepte_les_espaces():
    assert parse_places(' 3 ') == 3


def test_parse_places_texte_retourne_none():
    assert parse_places('abc') is None


def test_parse_places_absent_retourne_none():
    assert parse_places(None) is None


@pytest.mark.parametrize('places', [0, -5])
def test_validate_refuse_quantite_non_positive(places):
    message = validate_purchase(CLUB, COMPETITION, places)

    assert 'at least one place' in message


def test_validate_accepte_quantite_positive():
    assert validate_purchase(CLUB, COMPETITION, 1) is None
