"""Tests unitaires des regles d'achat de places."""

import pytest

from booking import confirmation_message, parse_places, validate_purchase

CLUB = {'points': '13'}
COMPETITION = {'numberOfPlaces': '25'}
COMPETITION_PETITE = {'numberOfPlaces': '3'}
CLUB_RICHE = {'points': '100'}
COMPETITION_GRANDE = {'numberOfPlaces': '100'}
CLUB_PAUVRE = {'points': '4'}
COMPETITION_COMPLETE = {'numberOfPlaces': '0'}


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


def test_validate_refuse_demande_superieure_au_stock():
    message = validate_purchase(CLUB, COMPETITION_PETITE, 4)

    assert 'not enough places' in message


def test_validate_accepte_demande_egale_au_stock():
    assert validate_purchase(CLUB, COMPETITION_PETITE, 3) is None


def test_validate_accepte_douze_places():
    assert validate_purchase(CLUB_RICHE, COMPETITION_GRANDE, 12) is None


def test_validate_refuse_plus_de_douze_places():
    message = validate_purchase(CLUB_RICHE, COMPETITION_GRANDE, 13)

    assert 'more than 12 places' in message


def test_validate_refuse_solde_de_points_insuffisant():
    message = validate_purchase(CLUB_PAUVRE, COMPETITION, 5)

    assert 'do not have enough points' in message


def test_validate_refuse_concours_complet():
    message = validate_purchase(CLUB, COMPETITION_COMPLETE, 1)

    assert 'competition is full' in message


@pytest.mark.parametrize('places, attendu', [
    (1, 'You have booked 1 place.'),
    (2, 'You have booked 2 places.'),
])
def test_confirmation_message_indique_le_nombre_de_places(places, attendu):
    assert attendu in confirmation_message(places)
