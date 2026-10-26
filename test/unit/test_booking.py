"""Tests unitaires des regles d'achat de places."""

from booking import parse_places


def test_parse_places_entier_valide():
    assert parse_places('3') == 3


def test_parse_places_accepte_les_espaces():
    assert parse_places(' 3 ') == 3


def test_parse_places_texte_retourne_none():
    assert parse_places('abc') is None


def test_parse_places_absent_retourne_none():
    assert parse_places(None) is None
